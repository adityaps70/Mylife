// Razorpay Subscriptions: monthly autopay (UPI Autopay / card / eNACH) for Self Streak Plus.
// Cashfree stays for one-off "pay one month" payments. Subscription state lives in the `meta` table:
//   rzp:<userId>    -> JSON { id, status, currentEnd, chargeAt, updated }
//   rzpsub:<subId>  -> userId
const DAY = 86400000;
const te = new TextEncoder();
const json = (d, status = 200) => new Response(JSON.stringify(d), { status, headers: { 'content-type': 'application/json', 'cache-control': 'no-store' } });
const err = (status, error) => json({ error }, status);
const hex = (buf) => [...new Uint8Array(buf)].map((b) => b.toString(16).padStart(2, '0')).join('');
async function hmac(secret, msg) { const k = await crypto.subtle.importKey('raw', te.encode(secret), { name: 'HMAC', hash: 'SHA-256' }, false, ['sign']); return hex(await crypto.subtle.sign('HMAC', k, te.encode(msg))); }
function same(a, b) { a = String(a || ''); b = String(b || ''); if (a.length !== b.length) return false; let r = 0; for (let i = 0; i < a.length; i++) r |= a.charCodeAt(i) ^ b.charCodeAt(i); return r === 0; }

export const rzpReady = (env) => !!(env.RAZORPAY_KEY_ID && env.RAZORPAY_KEY_SECRET);
async function rzp(env, path, init = {}) {
  const r = await fetch('https://api.razorpay.com/v1' + path, { ...init, headers: { authorization: 'Basic ' + btoa(env.RAZORPAY_KEY_ID + ':' + env.RAZORPAY_KEY_SECRET), 'content-type': 'application/json' } });
  const d = await r.json().catch(() => ({}));
  if (!r.ok) { console.error('razorpay', path, r.status, JSON.stringify(d).slice(0, 400)); const e = new Error(d?.error?.description || 'razorpay_error'); e.status = r.status; throw e; }
  return d;
}
const getMeta = async (env, k) => (await env.DB.prepare('SELECT v FROM meta WHERE k = ?').bind(k).first())?.v ?? null;
const setMeta = (env, k, v) => env.DB.prepare('INSERT INTO meta (k, v) VALUES (?, ?) ON CONFLICT(k) DO UPDATE SET v = excluded.v').bind(k, v).run();

async function ensurePlan(env) {
  const price = Number(env.PRICE_INR || 499), key = 'rzp_plan:' + price;
  const have = await getMeta(env, key); if (have) return have;
  const p = await rzp(env, '/plans', { method: 'POST', body: JSON.stringify({ period: 'monthly', interval: 1, item: { name: 'Self Streak Plus', amount: price * 100, currency: 'INR', description: 'Self Streak Plus · monthly' } }) });
  await setMeta(env, key, p.id); return p.id;
}
export async function autopayOf(env, uid) { const v = await getMeta(env, 'rzp:' + uid); try { return v ? JSON.parse(v) : null; } catch { return null; } }

// Bring our copy of a subscription (and the user's paid_until) in line with Razorpay's entity.
async function syncSub(env, s, uidHint) {
  const uid = uidHint || s?.notes?.user_id || (await getMeta(env, 'rzpsub:' + s.id)); if (!uid) return null;
  const rec = { id: s.id, status: s.status, currentEnd: s.current_end ? s.current_end * 1000 : null, chargeAt: s.charge_at ? s.charge_at * 1000 : null, updated: Date.now() };
  const prev = await autopayOf(env, uid);
  if (prev && prev.id === s.id && prev.cancelling && s.status === 'active') rec.cancelling = true;
  if (!prev || prev.id === s.id || !['active', 'authenticated'].includes(prev.status) || ['active', 'authenticated'].includes(s.status)) await setMeta(env, 'rzp:' + uid, JSON.stringify(rec));
  await setMeta(env, 'rzpsub:' + s.id, uid);
  if (s.status === 'active' && rec.currentEnd) {
    // Paid cycle: access runs to the end of the cycle plus a 1-day grace while the next debit clears.
    await env.DB.prepare("UPDATE users SET paid_until = MAX(paid_until, ?), plan = CASE WHEN plan = 'owner' THEN plan ELSE 'active' END WHERE id = ?").bind(rec.currentEnd + DAY, uid).run();
  }
  return rec;
}
async function recordPayment(env, uid, pay) {
  if (!pay?.id) return;
  await env.DB.prepare('INSERT OR IGNORE INTO payments (order_id, user_id, amount, status, created, paid_at) VALUES (?, ?, ?, ?, ?, ?)')
    .bind('rzp_' + pay.id, uid, Math.round((pay.amount || 0) / 100), 'paid', (pay.created_at || 0) * 1000 || Date.now(), Date.now()).run();
}

// Public (no session): Razorpay → us.
export async function rzpWebhook(req, env) {
  if (!env.RAZORPAY_WEBHOOK_SECRET) return err(404, 'not_found');
  const raw = await req.text(), sig = req.headers.get('x-razorpay-signature') || '';
  if (!same(await hmac(env.RAZORPAY_WEBHOOK_SECRET, raw), sig)) return err(401, 'bad_signature');
  let ev = {}; try { ev = JSON.parse(raw); } catch {}
  const s = ev?.payload?.subscription?.entity;
  if (s?.id) {
    const rec = await syncSub(env, s);
    const pay = ev?.payload?.payment?.entity;
    if (rec && ev.event === 'subscription.charged' && pay?.status === 'captured') await recordPayment(env, await getMeta(env, 'rzpsub:' + s.id), pay);
  }
  return json({ ok: true });
}

// Signed-in routes.
export async function rzpRoutes(req, env, p, m, body, u, url) {
  if (!p.startsWith('/api/billing/rzp/')) return null;
  if (!rzpReady(env)) return err(501, 'Autopay isn’t switched on yet.');
  if (p === '/api/billing/rzp/subscribe' && m === 'POST') {
    if (u.plan === 'owner') return err(400, 'You’re the owner. No subscription needed.');
    const cur = await autopayOf(env, u.id);
    if (cur && ['active', 'authenticated'].includes(cur.status)) return err(409, 'Autopay is already on for your account.');
    // If this person still has trial/paid time, the first charge waits until it runs out.
    const left = Math.max(Number(u.paid_until) || 0, u.plan === 'active' ? 0 : Number(u.trial_ends) || 0);
    const startAt = left > Date.now() + 2 * 3600e3 ? Math.floor(left / 1000) : undefined;
    const s = await rzp(env, '/subscriptions', { method: 'POST', body: JSON.stringify({ plan_id: await ensurePlan(env), total_count: 120, quantity: 1, customer_notify: 1, ...(startAt ? { start_at: startAt } : {}), notes: { user_id: u.id, email: u.email } }) });
    await setMeta(env, 'rzpsub:' + s.id, u.id);
    return json({ key: env.RAZORPAY_KEY_ID, subscriptionId: s.id, startAt: startAt ? startAt * 1000 : null, price: Number(env.PRICE_INR || 499) });
  }
  if (p === '/api/billing/rzp/verify' && m === 'POST') {
    const b = await body(), pid = String(b.razorpay_payment_id || ''), sid = String(b.razorpay_subscription_id || ''), sig = String(b.razorpay_signature || '');
    if (!pid || !sid || !same(await hmac(env.RAZORPAY_KEY_SECRET, pid + '|' + sid), sig)) return err(400, 'Couldn’t confirm the payment. If money was taken, it will show here within a few minutes.');
    if ((await getMeta(env, 'rzpsub:' + sid)) !== u.id) return err(403, 'This subscription belongs to another account.');
    const s = await rzp(env, '/subscriptions/' + sid);
    const rec = await syncSub(env, s, u.id);
    try { const pay = await rzp(env, '/payments/' + pid); if (pay.status === 'captured' && pay.amount >= 100 * Number(env.PRICE_INR || 499)) await recordPayment(env, u.id, pay); } catch {}
    return json({ ok: true, autopay: rec });
  }
  if (p === '/api/billing/rzp/cancel' && m === 'POST') {
    const cur = await autopayOf(env, u.id);
    if (!cur || !['active', 'authenticated', 'pending', 'halted'].includes(cur.status)) return err(404, 'Autopay isn’t on.');
    let s;
    try { s = await rzp(env, `/subscriptions/${cur.id}/cancel`, { method: 'POST', body: JSON.stringify({ cancel_at_cycle_end: cur.status === 'active' ? 1 : 0 }) }); }
    catch (e) { s = await rzp(env, `/subscriptions/${cur.id}/cancel`, { method: 'POST', body: JSON.stringify({ cancel_at_cycle_end: 0 }) }); }
    const rec = await syncSub(env, s, u.id);
    if (rec && s.status !== 'cancelled') { rec.cancelling = true; await setMeta(env, 'rzp:' + u.id, JSON.stringify(rec)); }
    return json({ ok: true, autopay: rec });
  }
  return err(404, 'not_found');
}
