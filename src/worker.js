// Self Streak API: accounts, per-user data, AI (Claude) with daily limits, push reminders, billing hooks.
import Anthropic from '@anthropic-ai/sdk';
import { sendPush } from './webpush.js';

const DAY = 86400000;
const MODEL = 'claude-haiku-5-5';
const te = new TextEncoder();
const hex = (buf) => [...new Uint8Array(buf)].map((b) => b.toString(16).padStart(2, '0')).join('');
const unhex = (h) => new Uint8Array(h.match(/.{2}/g).map((x) => parseInt(x, 16)));
const sha256 = async (s) => hex(await crypto.subtle.digest('SHA-256', te.encode(s)));
const randHex = (n) => hex(crypto.getRandomValues(new Uint8Array(n)));
const json = (d, status = 200, headers = {}) => new Response(JSON.stringify(d), { status, headers: { 'content-type': 'application/json', 'cache-control': 'no-store', ...headers } });
const err = (status, error, extra = {}) => json({ error, ...extra }, status);
const istDay = (t = Date.now()) => new Date(t + 5.5 * 3600e3).toISOString().slice(0, 10);

async function hashPassword(pw, saltHex) {
  const key = await crypto.subtle.importKey('raw', te.encode(pw), 'PBKDF2', false, ['deriveBits']);
  return hex(await crypto.subtle.deriveBits({ name: 'PBKDF2', hash: 'SHA-256', salt: unhex(saltHex), iterations: 100000 }, key, 256));
}
function safeEqual(a, b) { if (a.length !== b.length) return false; let r = 0; for (let i = 0; i < a.length; i++) r |= a.charCodeAt(i) ^ b.charCodeAt(i); return r === 0; }
function cookie(req, name) { const m = (req.headers.get('cookie') || '').match(new RegExp('(?:^|; )' + name + '=([^;]+)')); return m ? m[1] : null; }
function sessionCookie(req, token, maxAge) {
  const secure = new URL(req.url).protocol === 'https:' ? '; Secure' : '';
  return `ss_session=${token}; Path=/; HttpOnly; SameSite=Lax; Max-Age=${maxAge}${secure}`;
}
async function newSession(env, req, userId) {
  const token = randHex(32);
  await env.DB.prepare('INSERT INTO sessions (token_hash, user_id, expires) VALUES (?, ?, ?)').bind(await sha256(token), userId, Date.now() + 30 * DAY).run();
  return sessionCookie(req, token, 30 * 86400);
}
async function currentUser(env, req) {
  const token = cookie(req, 'ss_session'); if (!token) return null;
  const row = await env.DB.prepare('SELECT u.* FROM sessions s JOIN users u ON u.id = s.user_id WHERE s.token_hash = ? AND s.expires > ?').bind(await sha256(token), Date.now()).first();
  return row || null;
}
function planStatus(u) {
  const now = Date.now();
  if (u.plan === 'owner') return 'owner';
  if (u.paid_until > now) return 'active';
  if (u.trial_ends > now) return 'trial';
  return 'expired';
}
async function usageToday(env, uid) {
  const r = await env.DB.prepare('SELECT count FROM usage WHERE user_id = ? AND day = ?').bind(uid, istDay()).first();
  return r ? r.count : 0;
}
async function me(env, u) {
  const limit = Number(env.DAILY_AI_LIMIT || 20);
  return { user: { id: u.id, email: u.email, name: u.name, plan: u.plan, status: planStatus(u), trialEnds: u.trial_ends, paidUntil: u.paid_until, created: u.created },
    usage: { used: await usageToday(env, u.id), limit }, price: Number(env.PRICE_INR || 499), vapidPublicKey: env.VAPID_PUBLIC_KEY };
}

/* ---------------- AI tasks (prompts and schemas live on the server) ---------------- */
const BILL_CATS = ['Rent / Home', 'Utilities', 'Phone & Internet', 'Subscriptions', 'Insurance', 'Credit card', 'Tax', 'Fitness', 'Household help', 'Other'];
const LOG_KINDS = ['habit_done', 'habit_undo', 'steps', 'water_add', 'water_set', 'sleep', 'weight', 'expense', 'income', 'bill_paid', 'emi_paid', 'haircut', 'product_bought', 'goal_progress', 'checklist_done', 'journal', 'reminder_add', 'meal'];
const strList = (a, max = 60) => (Array.isArray(a) ? a : []).map((x) => String(x).slice(0, 80)).filter(Boolean).slice(0, max);
const obj = (props) => ({ type: 'object', additionalProperties: false, required: Object.keys(props), properties: props });
const S = { type: 'string' }, N = { type: 'number' };
const MEAL = obj({ name: S, items: { type: 'array', items: obj({ name: S, quantity: S }) }, calories: N, protein_g: N, carbs_g: N, fat_g: N, note: S });
function fileBlock(input) {
  const media = String(input.media || ''), data = String(input.data || '');
  if (!data || data.length > 30_000_000) throw new Error('bad_file');
  if (media === 'application/pdf') return { type: 'document', source: { type: 'base64', media_type: media, data } };
  if (/^image\/(jpeg|png|webp|gif)$/.test(media)) return { type: 'image', source: { type: 'base64', media_type: media, data } };
  throw new Error('bad_file');
}
const docProps = (kinds, catEnum) => ({ kind: { type: 'string', enum: kinds }, title: S, merchant: S, amount: N, bill_date: S, due_date: S, recurring: { type: 'boolean' }, frequency: { type: 'string', enum: ['monthly', 'quarterly', 'half-yearly', 'yearly', 'none'] }, bill_category: { type: 'string', enum: BILL_CATS }, spend_category: { type: 'string', enum: catEnum }, matched_bill: S, summary: S });
const docSchema = (kinds, catEnum) => obj(docProps(kinds, catEnum));
function buildTask(task, input) {
  const cats = strList(input.cats, 40);
  const catEnum = cats.length ? cats : ['Other'];
  switch (task) {
    case 'log': {
      const today = /^\d{4}-\d{2}-\d{2}$/.test(input.today || '') ? input.today : istDay();
      return {
        effort: 'low', maxTokens: 8000,
        system: `You turn what the user says or writes (English, Hindi or Hinglish) into updates for their personal life dashboard. Today is ${today}, a ${String(input.weekday || '').slice(0, 12)}. Use only ids that appear in the lists.
- "completed my daily steps", "10k done" → steps 10000 and habit_done for the steps habit. "8k" means 8000.
- Water: glasses → water_add. Litres → glasses = litres × 4. "finished my water" → water_set 12.
- "gym", "workout", "exercise" → habit_done for the gym habit. Match other habits by meaning.
- Money spent → expense (value = rupees, text = who was paid, ref = best budget category). Money received → income.
- Paying a known bill → bill_paid with the bill id. Paying an EMI → emi_paid with the loan id.
- Food or drink eaten → meal: text = short meal name, value = estimated calories, protein/carbs/fat = estimated grams for typical Indian portions.
- "got a haircut" → haircut. Bought a listed grooming product → product_bought.
- A note about the day → journal (value = mood 1-5 if they said how the day felt, else 0).
- "remind me to …" → reminder_add with a date.
Never invent things the user didn't say. If nothing fits, return no actions. reply: one short friendly spoken sentence.`,
        content: [{ type: 'text', text: String(input.context || '').slice(0, 20000) + '\n\nWHAT I SAID: ' + String(input.text || '').slice(0, 4000) }],
        schema: obj({ reply: S, actions: { type: 'array', items: obj({ kind: { type: 'string', enum: LOG_KINDS }, ref: S, value: N, text: S, date: S, protein: N, carbs: N, fat: N }) } }),
      };
    }
    case 'statement':
      return {
        effort: 'medium', maxTokens: 64000, stream: true,
        system: `You read Indian bank statements for a personal budgeting app. Amounts are in rupees. Return every transaction row, never opening/closing balances or totals. direction "out" = withdrawal/debit, "in" = deposit/credit.
Category rules: salary credits → "Salary (already counted)". Transfers to the user's own accounts, FDs/RDs, sweeps, SIPs, mutual funds, brokers, NPS/PPF → "Transfer / ignore". Credit-card bill payments, rent, electricity, broadband, mobile recharge, LPG, insurance premiums, house tax → "Bill payment". Loan EMIs → "EMI". Refunds, cashback, interest and other credits → "Income". Everything else → the closest category, else "Other".
payee: a short readable name (e.g. "Swiggy", "Rahul Sharma"), never UPI ids or reference numbers.`,
        content: [fileBlock(input), { type: 'text', text: 'Extract every transaction from this statement.' }],
        schema: obj({ bank: S, transactions: { type: 'array', items: obj({ date: { type: 'string', description: 'YYYY-MM-DD' }, description: S, payee: S, amount: N, direction: { type: 'string', enum: ['in', 'out'] }, category: { type: 'string', enum: catEnum } }) } }),
      };
    case 'categorise':
      return {
        effort: 'low', maxTokens: 32000, stream: true,
        system: 'Categorise Indian bank transactions for a budgeting app. Salary → "Salary (already counted)"; own-account transfers, SIPs, investments → "Transfer / ignore"; bills (rent, electricity, recharge, insurance, card bill) → "Bill payment"; loan EMIs → "EMI"; refunds/interest → "Income". payee: short readable name.',
        content: [{ type: 'text', text: 'Each line: index, direction, amount, narration.\n' + strList(input.lines, 400).join('\n') }],
        schema: obj({ items: { type: 'array', items: obj({ i: { type: 'integer' }, category: { type: 'string', enum: catEnum }, payee: S }) } }),
      };
    case 'receipt':
      return {
        effort: 'low', maxTokens: 8000,
        system: `You read photos or PDFs of Indian bills and receipts. Decide if it is a bill still to be paid (has a due date / amount payable), a receipt for something already paid, or other. Dates as YYYY-MM-DD, empty if absent. Amount in rupees (total payable or total paid). Known bills the user already tracks: ${strList(input.bills, 40).join(' | ') || 'none'} — set matched_bill to the exact name if this is one of them, else empty.`,
        content: [fileBlock(input), { type: 'text', text: 'Read this bill or receipt.' }],
        schema: docSchema(['bill', 'receipt', 'other'], catEnum),
      };
    case 'snap':
      return {
        effort: 'low', maxTokens: 8000,
        system: `You look at one photo or PDF a user of an Indian life-tracking app snapped and decide what it is: "meal" (food or drink they ate), "bill" (still to be paid: has an amount payable / due date, e.g. electricity, phone, card statement), "receipt" (already paid: shop/restaurant/online order receipt, UPI payment screenshot), "statement" (a bank or card statement with many transactions), or "other". confident=false if you genuinely cannot tell; then put a short friendly question in question. Fill meal only for meals (realistic Indian portions, calories and grams of protein, carbs, fat), and doc only for bills and receipts (dates YYYY-MM-DD or empty, amount in rupees). Known bills: ${strList(input.bills, 40).join(' | ') || 'none'} — set doc.matched_bill to the exact name if it is one of them. For unused sections return empty strings and zeros.`,
        content: [fileBlock(input), { type: 'text', text: 'What is this? ' + String(input.note || '').slice(0, 300) }],
        schema: obj({ kind: { type: 'string', enum: ['meal', 'bill', 'receipt', 'statement', 'other'] }, confident: { type: 'boolean' }, question: S, meal: MEAL, doc: docSchema(['bill', 'receipt', 'other'], catEnum) }),
      };
    case 'meal_photo':
      return {
        effort: 'low', maxTokens: 6000,
        system: 'Estimate the nutrition of the food in this photo for a fitness app used in India. Identify each item and a realistic portion, then estimate total calories and grams of protein, carbs and fat. Be realistic, not optimistic. note: one short tip (e.g. how to add protein).',
        content: [fileBlock(input), { type: 'text', text: 'What did I eat? ' + String(input.note || '').slice(0, 300) }],
        schema: MEAL,
      };
    case 'meal_text':
      return {
        effort: 'low', maxTokens: 6000,
        system: 'Estimate the nutrition of a meal described in English, Hindi or Hinglish, using typical Indian home portions unless stated. Return total calories and grams of protein, carbs and fat. note: one short tip.',
        content: [{ type: 'text', text: String(input.text || '').slice(0, 1000) }],
        schema: MEAL,
      };
  }
  return null;
}
async function runAI(env, spec) {
  const client = new Anthropic({ apiKey: env.ANTHROPIC_API_KEY });
  const params = { model: MODEL, max_tokens: spec.maxTokens, system: spec.system, messages: [{ role: 'user', content: spec.content }], output_config: { effort: spec.effort, format: { type: 'json_schema', schema: spec.schema } } };
  const msg = spec.stream ? await client.messages.stream(params).finalMessage() : await client.messages.create(params);
  if (msg.stop_reason === 'refusal') return { error: 'refused' };
  if (msg.stop_reason === 'max_tokens') return { error: 'too_long' };
  const text = msg.content.filter((b) => b.type === 'text').map((b) => b.text).join('');
  return { result: JSON.parse(text) };
}

/* ---------------- API router ---------------- */
async function api(req, env, url) {
  const p = url.pathname, m = req.method;
  if (m !== 'GET') {
    const origin = req.headers.get('origin');
    if (origin && origin !== url.origin) return err(403, 'bad_origin');
  }
  const body = async () => { try { return await req.json(); } catch { return {}; } };

  if (p === '/api/signup' && m === 'POST') {
    const b = await body(), email = String(b.email || '').trim().toLowerCase(), pw = String(b.password || ''), name = String(b.name || '').trim().slice(0, 60);
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) return err(400, 'Enter a valid email address.');
    if (pw.length < 8) return err(400, 'Use at least 8 characters for your password.');
    if (await env.DB.prepare('SELECT 1 FROM users WHERE email = ?').bind(email).first()) return err(409, 'An account with this email already exists. Log in instead.');
    const first = !(await env.DB.prepare('SELECT 1 FROM users LIMIT 1').first());
    const id = crypto.randomUUID(), salt = randHex(16), now = Date.now();
    await env.DB.prepare('INSERT INTO users (id, email, name, pass_hash, salt, plan, trial_ends, created) VALUES (?, ?, ?, ?, ?, ?, ?, ?)')
      .bind(id, email, name, await hashPassword(pw, salt), salt, first ? 'owner' : 'trial', now + Number(env.TRIAL_DAYS || 7) * DAY, now).run();
    const u = await env.DB.prepare('SELECT * FROM users WHERE id = ?').bind(id).first();
    return json({ ...(await me(env, u)), isNew: true }, 200, { 'set-cookie': await newSession(env, req, id) });
  }
  if (p === '/api/login' && m === 'POST') {
    const b = await body(), email = String(b.email || '').trim().toLowerCase(), pw = String(b.password || '');
    const u = await env.DB.prepare('SELECT * FROM users WHERE email = ?').bind(email).first();
    if (!u) { await hashPassword(pw, '00'.repeat(16)); return err(401, 'Wrong email or password.'); }
    if (u.locked_until > Date.now()) return err(429, 'Too many attempts. Try again in a few minutes.');
    if (!safeEqual(await hashPassword(pw, u.salt), u.pass_hash)) {
      const fails = u.fail_count + 1;
      await env.DB.prepare('UPDATE users SET fail_count = ?, locked_until = ? WHERE id = ?').bind(fails >= 5 ? 0 : fails, fails >= 5 ? Date.now() + 10 * 60000 : 0, u.id).run();
      return err(401, 'Wrong email or password.');
    }
    await env.DB.prepare('UPDATE users SET fail_count = 0, locked_until = 0 WHERE id = ?').bind(u.id).run();
    return json(await me(env, u), 200, { 'set-cookie': await newSession(env, req, u.id) });
  }
  if (p === '/api/logout' && m === 'POST') {
    const t = cookie(req, 'ss_session');
    const b = await body();
    if (t) {
      const s = await env.DB.prepare('SELECT user_id FROM sessions WHERE token_hash = ?').bind(await sha256(t)).first();
      if (s && b.endpoint) await env.DB.prepare('DELETE FROM push_subs WHERE user_id = ? AND endpoint = ?').bind(s.user_id, String(b.endpoint)).run();
      await env.DB.prepare('DELETE FROM sessions WHERE token_hash = ?').bind(await sha256(t)).run();
    }
    return json({ ok: true }, 200, { 'set-cookie': sessionCookie(req, '', 0) });
  }

  const u = await currentUser(env, req);
  if (!u) return err(401, 'not_signed_in');

  if (p === '/api/me' && m === 'GET') return json(await me(env, u));
  if (p === '/api/profile' && m === 'POST') {
    const b = await body();
    await env.DB.prepare('UPDATE users SET name = ? WHERE id = ?').bind(String(b.name || '').slice(0, 60), u.id).run();
    return json({ ok: true });
  }
  if (p === '/api/password' && m === 'POST') {
    const b = await body();
    if (!safeEqual(await hashPassword(String(b.current || ''), u.salt), u.pass_hash)) return err(400, 'Current password is wrong.');
    if (String(b.next || '').length < 8) return err(400, 'Use at least 8 characters.');
    const salt = randHex(16);
    await env.DB.prepare('UPDATE users SET pass_hash = ?, salt = ? WHERE id = ?').bind(await hashPassword(String(b.next), salt), salt, u.id).run();
    await env.DB.prepare('DELETE FROM sessions WHERE user_id = ? AND token_hash <> ?').bind(u.id, await sha256(cookie(req, 'ss_session') || '')).run();
    return json({ ok: true });
  }
  if (p === '/api/account' && m === 'DELETE') {
    for (const t of ['sessions', 'user_data', 'usage', 'push_subs', 'push_schedule']) await env.DB.prepare(`DELETE FROM ${t} WHERE user_id = ?`).bind(u.id).run();
    await env.DB.prepare('DELETE FROM users WHERE id = ?').bind(u.id).run();
    return json({ ok: true }, 200, { 'set-cookie': sessionCookie(req, '', 0) });
  }
  if (p === '/api/data') {
    if (m === 'GET') {
      const r = await env.DB.prepare('SELECT json, updated FROM user_data WHERE user_id = ?').bind(u.id).first();
      return json(r ? { data: JSON.parse(r.json), updated: r.updated } : { data: null, updated: 0 });
    }
    if (m === 'PUT') {
      const text = await req.text();
      if (text.length > 1_900_000) return err(413, 'Your data is too large to sync.');
      let b; try { b = JSON.parse(text); } catch { return err(400, 'bad_json'); }
      const updated = Number(b.updated) || Date.now();
      if (b.base != null) {
        const cur = await env.DB.prepare('SELECT json, updated FROM user_data WHERE user_id = ?').bind(u.id).first();
        if (cur && cur.updated > Number(b.base)) return json({ conflict: true, data: JSON.parse(cur.json), updated: cur.updated }, 409);
      }
      await env.DB.prepare('INSERT INTO user_data (user_id, json, updated) VALUES (?, ?, ?) ON CONFLICT(user_id) DO UPDATE SET json = excluded.json, updated = excluded.updated')
        .bind(u.id, JSON.stringify(b.data ?? null), updated).run();
      return json({ ok: true, updated });
    }
  }
  if (p === '/api/ai' && m === 'POST') {
    if (planStatus(u) === 'expired') return err(402, 'Your free trial has ended. Subscribe to keep using AI features.');
    const b = await body(), spec = (() => { try { return buildTask(String(b.task || ''), b.input || {}); } catch { return 'bad_file'; } })();
    if (spec === 'bad_file') return err(400, 'That file type isn’t supported. Use a PDF or a photo (JPG/PNG).');
    if (!spec) return err(400, 'unknown_task');
    const limit = Number(env.DAILY_AI_LIMIT || 20), day = istDay();
    const row = await env.DB.prepare('INSERT INTO usage (user_id, day, count) VALUES (?, ?, 1) ON CONFLICT(user_id, day) DO UPDATE SET count = count + 1 WHERE count < ? RETURNING count').bind(u.id, day, limit).first();
    if (!row) return err(429, `You’ve used all ${limit} AI actions for today. They reset at midnight.`, { used: limit, limit });
    try {
      const out = await runAI(env, spec);
      if (out.error) return err(422, out.error === 'refused' ? 'The AI declined this one.' : 'That was too long to read in one go. Try a shorter statement period.', { used: row.count, limit });
      return json({ result: out.result, used: row.count, limit });
    } catch (e) {
      // Refund only when the request never produced output (overloaded / network / auth); a bad reply still cost tokens.
      const status = e?.status || 0, upstream = status >= 400 || e?.name === 'APIConnectionError' || /connection|fetch/i.test(String(e?.message || ''));
      if (upstream) await env.DB.prepare('UPDATE usage SET count = MAX(count - 1, 0) WHERE user_id = ? AND day = ?').bind(u.id, day).run();
      return err(502, status === 429 || status === 529 ? 'The AI is busy right now. Try again in a minute.' : 'The AI couldn’t process that. Please try again.', { used: upstream ? row.count - 1 : row.count, limit });
    }
  }
  if (p === '/api/push/subscribe' && m === 'POST') {
    const b = await body();
    if (!/^https:\/\//.test(b.endpoint || '') || !b.keys?.p256dh || !b.keys?.auth) return err(400, 'bad_subscription');
    await env.DB.prepare('INSERT INTO push_subs (endpoint, user_id, p256dh, auth, created) VALUES (?, ?, ?, ?, ?) ON CONFLICT(endpoint) DO UPDATE SET user_id = excluded.user_id, p256dh = excluded.p256dh, auth = excluded.auth')
      .bind(b.endpoint, u.id, b.keys.p256dh, b.keys.auth, Date.now()).run();
    return json({ ok: true });
  }
  if (p === '/api/push/unsubscribe' && m === 'POST') {
    const b = await body();
    await env.DB.prepare('DELETE FROM push_subs WHERE endpoint = ? AND user_id = ?').bind(String(b.endpoint || ''), u.id).run();
    return json({ ok: true });
  }
  if (p === '/api/push/schedule' && m === 'PUT') {
    const b = await body(), now = Date.now();
    const items = (Array.isArray(b.items) ? b.items : []).filter((i) => Number(i.at) > now - 3600e3 && Number(i.at) < now + 3 * DAY).slice(0, 300).map((i) => ({
      at: Number(i.at), title: String(i.title || '').slice(0, 120), body: String(i.body || '').slice(0, 400), url: String(i.url || './').slice(0, 200), tag: String(i.tag || '').slice(0, 120),
      actions: (Array.isArray(i.actions) ? i.actions : []).slice(0, 2).map((a) => ({ action: String(a.action).slice(0, 20), title: String(a.title).slice(0, 30) })),
      acts: Object.fromEntries(Object.entries(i.acts || {}).slice(0, 2).map(([k, v]) => [String(k).slice(0, 20), String(v).slice(0, 120)])),
    }));
    await env.DB.prepare('INSERT INTO push_schedule (user_id, items, last_sent, updated) VALUES (?, ?, ?, ?) ON CONFLICT(user_id) DO UPDATE SET items = excluded.items, updated = excluded.updated')
      .bind(u.id, JSON.stringify(items), now, now).run();
    return json({ ok: true, count: items.length });
  }
  if (p === '/api/push/test' && m === 'POST') {
    const subs = (await env.DB.prepare('SELECT * FROM push_subs WHERE user_id = ?').bind(u.id).all()).results;
    let sent = 0;
    for (const s of subs) { const st = await sendPush(s, { title: 'Push is working 🎉', body: 'Self Streak can now remind you even when the app is closed.', tag: 'push-test', url: './#/notify' }, env); if (st < 300) sent++; else if (st === 404 || st === 410) await env.DB.prepare('DELETE FROM push_subs WHERE endpoint = ?').bind(s.endpoint).run(); }
    return json({ ok: true, sent, devices: subs.length });
  }
  if (p === '/api/billing/checkout' && m === 'POST') {
    return err(501, 'Online payments are launching soon. We’ll email you as soon as you can subscribe.');
  }
  return err(404, 'not_found');
}

/* ---------------- scheduled: send due reminders as push notifications ---------------- */
async function sendDuePushes(env) {
  const now = Date.now();
  const rows = (await env.DB.prepare('SELECT s.user_id, s.items, s.last_sent FROM push_schedule s WHERE EXISTS (SELECT 1 FROM push_subs p WHERE p.user_id = s.user_id)').all()).results;
  for (const r of rows) {
    const since = Math.max(Number(r.last_sent) || 0, now - 20 * 60000);
    const due = JSON.parse(r.items).filter((i) => i.at > since && i.at <= now);
    if (!due.length) continue;
    const msg = due.length === 1 ? due[0] : { title: `${due.length} reminders`, body: due.map((i) => '• ' + i.title).join('\n'), tag: due[0].tag, url: due[0].url };
    const subs = (await env.DB.prepare('SELECT * FROM push_subs WHERE user_id = ?').bind(r.user_id).all()).results;
    for (const s of subs) {
      try { const st = await sendPush(s, msg, env); if (st === 404 || st === 410) await env.DB.prepare('DELETE FROM push_subs WHERE endpoint = ?').bind(s.endpoint).run(); } catch (e) { /* try again next run */ }
    }
    await env.DB.prepare('UPDATE push_schedule SET last_sent = ? WHERE user_id = ?').bind(now, r.user_id).run();
  }
  await env.DB.prepare('DELETE FROM sessions WHERE expires < ?').bind(now).run();
}

export default {
  async fetch(req, env) {
    const url = new URL(req.url);
    if (url.pathname.startsWith('/api/')) {
      try { return await api(req, env, url); } catch (e) { console.error(e); return err(500, 'Something went wrong. Please try again.'); }
    }
    return env.ASSETS.fetch(req);
  },
  async scheduled(event, env, ctx) { ctx.waitUntil(sendDuePushes(env)); },
};
