// Self Streak "keep coming back" layer: streak sync, weekly leagues, friends + friend streaks,
// referrals, streak-at-risk pushes and the Sunday recap. The app computes XP/streaks from the
// user's own data; the server only keeps the small summary it needs to compare people.
import { sendPush } from './webpush.js';

const DAY = 86400000;
const GRACE = 3 * DAY;
// SQL fragment: user `u` still has Plus (owner, paid, trial, or within the grace period). Bind (cut, cut).
const PLUS_SQL = "(u.plan = 'owner' OR u.paid_until > ? OR u.trial_ends > ?)";
const IST = 5.5 * 3600e3;
export const TIERS = ['Bronze', 'Silver', 'Gold', 'Sapphire', 'Diamond'];
const GROUP = 20;
const json = (d, status = 200) => new Response(JSON.stringify(d), { status, headers: { 'content-type': 'application/json', 'cache-control': 'no-store' } });
const err = (status, error) => json({ error }, status);
const istDay = (t = Date.now()) => new Date(t + IST).toISOString().slice(0, 10);
const addDay = (s, n) => new Date(Date.parse(s + 'T00:00:00Z') + n * DAY).toISOString().slice(0, 10);
// Monday (IST) of the week that contains t.
export function weekKey(t = Date.now()) { const d = new Date(t + IST); const dow = (d.getUTCDay() + 6) % 7; return new Date(Date.UTC(d.getUTCFullYear(), d.getUTCMonth(), d.getUTCDate() - dow)).toISOString().slice(0, 10); }
const CODE_CH = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789';
const newCode = () => [...crypto.getRandomValues(new Uint8Array(6))].map((b) => CODE_CH[b % CODE_CH.length]).join('');
const shortName = (name, id) => { const p = String(name || '').trim().split(/\s+/).filter(Boolean); if (!p.length) return 'Streaker ' + String(id).slice(0, 4).toUpperCase(); return p[0].slice(0, 16) + (p[1] ? ' ' + p[1][0].toUpperCase() + '.' : ''); };
const parse = (s, d) => { try { return JSON.parse(s) ?? d; } catch { return d; } };

export async function ensureGame(env, uid) {
  let g = await env.DB.prepare('SELECT * FROM game WHERE user_id = ?').bind(uid).first();
  if (g) return g;
  for (let i = 0; i < 5; i++) {
    try { await env.DB.prepare('INSERT INTO game (user_id, code, updated) VALUES (?, ?, ?)').bind(uid, newCode(), Date.now()).run(); break; } catch (e) { if (!/UNIQUE/i.test(String(e))) throw e; }
  }
  return env.DB.prepare('SELECT * FROM game WHERE user_id = ?').bind(uid).first();
}
async function befriend(env, a, b) {
  if (!a || !b || a === b) return;
  const now = Date.now();
  await env.DB.batch([
    env.DB.prepare('INSERT OR IGNORE INTO friends (a, b, created) VALUES (?, ?, ?)').bind(a, b, now),
    env.DB.prepare('INSERT OR IGNORE INTO friends (a, b, created) VALUES (?, ?, ?)').bind(b, a, now),
  ]);
}
// Called right after a new account is created with ?ref=CODE. Both get 7 free days (referrer capped at 12 rewards).
export async function applyReferral(env, newId, code) {
  code = String(code || '').trim().toUpperCase();
  if (!/^[A-Z0-9]{6}$/.test(code)) return;
  const ref = await env.DB.prepare('SELECT user_id FROM game WHERE code = ?').bind(code).first();
  if (!ref || ref.user_id === newId) return;
  const g = await ensureGame(env, newId);
  if (g.ref_by) return;
  const now = Date.now();
  await env.DB.prepare('UPDATE game SET ref_by = ? WHERE user_id = ?').bind(ref.user_id, newId).run();
  await env.DB.prepare('UPDATE users SET trial_ends = MAX(trial_ends, ?) + ? WHERE id = ?').bind(now, 7 * DAY, newId).run();
  const n = (await env.DB.prepare('SELECT COUNT(*) AS n FROM game WHERE ref_by = ?').bind(ref.user_id).first()).n;
  if (n <= 12) {
    const r = await env.DB.prepare('SELECT paid_until, trial_ends, plan FROM users WHERE id = ?').bind(ref.user_id).first();
    if (r && r.plan !== 'owner') {
      if (r.paid_until > now) await env.DB.prepare('UPDATE users SET paid_until = paid_until + ? WHERE id = ?').bind(7 * DAY, ref.user_id).run();
      else await env.DB.prepare('UPDATE users SET trial_ends = MAX(trial_ends, ?) + ? WHERE id = ?').bind(now, 7 * DAY, ref.user_id).run();
    }
  }
  await befriend(env, newId, ref.user_id);
  await pushTo(env, ref.user_id, { title: 'Your invite worked 🎉', body: 'A friend joined Self Streak with your link. You both got 7 free days, and they’re now on your friends list.', tag: 'ref', url: './#/streak' });
}

async function pushTo(env, uid, msg) {
  const subs = (await env.DB.prepare('SELECT * FROM push_subs WHERE user_id = ?').bind(uid).all()).results;
  let sent = 0;
  for (const s of subs) {
    try { const st = await sendPush(s, msg, env); if (st < 300) sent++; else if (st === 404 || st === 410) await env.DB.prepare('DELETE FROM push_subs WHERE endpoint = ?').bind(s.endpoint).run(); } catch (e) { /* skip */ }
  }
  return sent;
}

// Together-streak: consecutive days (ending today or yesterday) on which both people were active.
function together(a, b) {
  const A = new Set(a), B = new Set(b), t = istDay();
  let d = A.has(t) && B.has(t) ? t : addDay(t, -1), n = 0;
  while (A.has(d) && B.has(d) && n < 400) { n++; d = addDay(d, -1); }
  return n;
}

async function leagueOf(env, g, wk) {
  const since = addDay(istDay(), -14);
  const rows = (await env.DB.prepare(`SELECT g.user_id, u.name, g.streak, CASE WHEN g.week_key = ? THEN g.week_xp ELSE 0 END AS xp
      FROM game g JOIN users u ON u.id = g.user_id WHERE g.tier = ? AND g.board = 1 AND (g.last_active >= ? OR g.user_id = ?) AND (${PLUS_SQL} OR g.user_id = ?) ORDER BY g.user_id`).bind(wk, g.tier, since, g.user_id, Date.now() - GRACE, Date.now() - GRACE, g.user_id).all()).results;
  const i = rows.findIndex((r) => r.user_id === g.user_id);
  if (i < 0) return { tier: g.tier, name: TIERS[g.tier], members: [], hidden: true };
  const grp = rows.slice(Math.floor(i / GROUP) * GROUP, Math.floor(i / GROUP) * GROUP + GROUP).sort((a, b) => b.xp - a.xp || a.user_id.localeCompare(b.user_id));
  const n = grp.length, up = g.tier < 4 ? Math.min(5, Math.max(1, Math.ceil(n / 4))) : 0, down = g.tier > 0 && n >= 8 ? Math.min(5, Math.floor(n / 4)) : 0;
  const end = Date.parse(addDay(wk, 7) + 'T00:00:00Z') - IST;
  return { tier: g.tier, name: TIERS[g.tier], up, down, endsAt: end, members: grp.map((r, k) => ({ name: shortName(r.name, r.user_id), xp: r.xp, streak: r.streak, me: r.user_id === g.user_id, rank: k + 1 })) };
}

export async function gameRoutes(req, env, p, m, body, u) {
  if (p === '/api/game' && m === 'PUT') {
    const b = await body();
    const g = await ensureGame(env, u.id);
    const days = (Array.isArray(b.days) ? b.days : []).map(String).filter((s) => /^\d{4}-\d{2}-\d{2}$/.test(s)).slice(-120);
    const wk = weekKey(), n = (v, max = 1e7) => Math.max(0, Math.min(max, Math.round(Number(v) || 0)));
    const stats = b.stats && typeof b.stats === 'object' ? JSON.stringify(b.stats).slice(0, 2000) : g.stats;
    await env.DB.prepare(`UPDATE game SET streak = ?, best = ?, last_active = ?, days = ?, xp = ?, week_key = ?, week_xp = ?, freezes = ?, board = ?, recap = ?, risk = ?, stats = ?, updated = ? WHERE user_id = ?`)
      .bind(n(b.streak, 5000), n(b.best, 5000), /^\d{4}-\d{2}-\d{2}$/.test(b.lastActive) ? b.lastActive : g.last_active, JSON.stringify(days), n(b.xp), wk, b.weekKey === wk ? n(b.weekXP, 50000) : 0,
        n(b.freezes, 2), b.board === false ? 0 : 1, b.recap === false ? 0 : 1, b.risk === false ? 0 : 1, stats, Date.now(), u.id).run();
    return json({ ok: true, code: g.code });
  }
  if (p === '/api/game/social' && m === 'GET') {
    const g = await ensureGame(env, u.id), wk = weekKey();
    const friends = (await env.DB.prepare(`SELECT f.b AS id, u.name, g.streak, g.days, g.last_active FROM friends f JOIN users u ON u.id = f.b LEFT JOIN game g ON g.user_id = f.b WHERE f.a = ? ORDER BY f.created`).bind(u.id).all()).results;
    const mine = parse(g.days, []), t = istDay();
    const refs = (await env.DB.prepare('SELECT COUNT(*) AS n FROM game WHERE ref_by = ?').bind(u.id).first()).n;
    return json({
      code: g.code, tier: g.tier, tierName: TIERS[g.tier], board: !!g.board, recap: !!g.recap, risk: !!g.risk, refs, result: parse(g.result, null), week: wk,
      league: await leagueOf(env, g, wk),
      friends: friends.map((f) => ({ id: f.id, name: shortName(f.name, f.id), streak: f.last_active && f.last_active >= addDay(t, -1) ? f.streak || 0 : 0, today: f.last_active === t, together: together(mine, parse(f.days, [])) })),
    });
  }
  if (p === '/api/game/friend' && m === 'POST') {
    const b = await body(), code = String(b.code || '').trim().toUpperCase().replace(/^.*REF=/, '');
    const f = await env.DB.prepare('SELECT user_id FROM game WHERE code = ?').bind(code).first();
    if (!f) return err(404, 'No one has that friend code. Check it and try again.');
    if (f.user_id === u.id) return err(400, 'That’s your own code. Share it with a friend instead.');
    const c = (await env.DB.prepare('SELECT COUNT(*) AS n FROM friends WHERE a = ?').bind(u.id).first()).n;
    if (c >= 50) return err(400, 'You can have up to 50 friends.');
    await ensureGame(env, u.id); await befriend(env, u.id, f.user_id);
    await pushTo(env, f.user_id, { title: `${shortName(u.name, u.id)} added you on Self Streak 🔥`, body: 'Keep your streaks going together. Open Self Streak to see your friend streak.', tag: 'friend', url: './#/streak' });
    return json({ ok: true });
  }
  if (p === '/api/game/friend' && m === 'DELETE') {
    const b = await body(), id = String(b.id || '');
    await env.DB.batch([env.DB.prepare('DELETE FROM friends WHERE a = ? AND b = ?').bind(u.id, id), env.DB.prepare('DELETE FROM friends WHERE a = ? AND b = ?').bind(id, u.id)]);
    return json({ ok: true });
  }
  if (p === '/api/game/nudge' && m === 'POST') {
    const b = await body(), id = String(b.id || '');
    if (!(await env.DB.prepare('SELECT 1 FROM friends WHERE a = ? AND b = ?').bind(u.id, id).first())) return err(404, 'Not on your friends list.');
    const k = `nudge:${u.id}:${id}:${istDay()}`;
    const ins = await env.DB.prepare('INSERT OR IGNORE INTO meta (k, v) VALUES (?, ?)').bind(k, String(Date.now())).run();
    if (!ins.meta.changes) return err(429, 'You already nudged them today.');
    const sent = await pushTo(env, id, { title: `${shortName(u.name, u.id)} nudged you 👋`, body: 'Your streak is waiting. One small thing today keeps it alive 🔥', tag: 'nudge', url: './#/streak' });
    return json({ ok: true, sent });
  }
  if (p === '/api/game/seen' && m === 'POST') {
    await env.DB.prepare('UPDATE game SET result = NULL WHERE user_id = ?').bind(u.id).run();
    return json({ ok: true });
  }
  return null;
}

/* ---------------- scheduled jobs (worker cron runs every 5 minutes) ---------------- */
async function once(env, k) { const r = await env.DB.prepare('INSERT OR IGNORE INTO meta (k, v) VALUES (?, ?)').bind(k, String(Date.now())).run(); return !!r.meta.changes; }

async function streakRisk(env, late) {
  const t = istDay(), y = addDay(t, -1);
  const rows = (await env.DB.prepare(`SELECT g.user_id, g.streak, g.freezes FROM game g WHERE g.risk = 1 AND g.streak >= ? AND g.last_active = ? AND (g.risk_sent IS NULL OR g.risk_sent <> ?)
      AND EXISTS (SELECT 1 FROM push_subs p WHERE p.user_id = g.user_id)
      AND EXISTS (SELECT 1 FROM users u WHERE u.id = g.user_id AND ${PLUS_SQL})`).bind(late ? 3 : 1, y, t + (late ? 'L' : ''), Date.now() - GRACE, Date.now() - GRACE).all()).results;
  for (const r of rows) {
    const msg = late
      ? { title: `⏰ 90 minutes left for your ${r.streak}-day streak`, body: r.freezes ? 'A streak freeze will cover you, but one glass of water keeps it for real.' : 'Log one thing (a glass of water counts) before midnight to keep it.', tag: 'streak-risk', url: './#/streak' }
      : { title: `🔥 Your ${r.streak}-day streak ends at midnight`, body: 'One small thing saves it: a glass of water, a habit tick or a meal photo.', tag: 'streak-risk', url: './#/streak' };
    await pushTo(env, r.user_id, msg);
    await env.DB.prepare('UPDATE game SET risk_sent = ? WHERE user_id = ?').bind(t + (late ? 'L' : ''), r.user_id).run();
  }
}

const escH = (s) => String(s ?? '').replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
function recapMail(name, s, streak, tier) {
  const rows = [['🔥 Streak', `${streak} day${streak === 1 ? '' : 's'}`], ['⭐ XP this week', s.xp], ['📅 Active days', `${s.active || 0} of 7`], ['✅ Habits ticked', s.habits || 0], ['💧 Glasses of water', s.water || 0], ['🍽️ Meals logged', s.meals || 0], ['₹ Spent', '₹' + Math.round(s.spent || 0).toLocaleString('en-IN')], ['🏆 League', tier]];
  const html = `<div style="font-family:system-ui,sans-serif;background:#09090b;color:#f4f4f5;padding:28px"><div style="max-width:480px;margin:auto;background:#141418;border:1px solid #26262c;border-radius:20px;padding:28px">
  <div style="font-size:13px;color:#a1a1aa;letter-spacing:.06em">YOUR WEEK ON SELF STREAK</div><h1 style="font-size:26px;margin:8px 0 4px">Nice week, ${escH(name)}!</h1>
  <p style="color:#a1a1aa;margin:0 0 18px">${escH(s.headline || 'Here’s what you did this week.')}</p>
  <table style="width:100%;border-collapse:collapse">${rows.map(([a, b]) => `<tr><td style="padding:10px 0;border-top:1px solid #26262c">${a}</td><td style="padding:10px 0;border-top:1px solid #26262c;text-align:right;font-weight:700">${escH(b)}</td></tr>`).join('')}</table>
  <a href="https://selfstreak.com/app#/streak" style="display:block;text-align:center;margin-top:22px;background:#d7f64a;color:#10120a;font-weight:800;padding:14px;border-radius:999px;text-decoration:none">Start next week strong →</a>
  <p style="font-size:12px;color:#71717a;margin-top:18px">You get this every Sunday. Turn it off in Self Streak → Streak &amp; rewards → Weekly recap.</p></div></div>`;
  const text = `Your week on Self Streak\n\n${rows.map(([a, b]) => `${a}: ${b}`).join('\n')}\n\nhttps://selfstreak.com/app#/streak\nTurn off: Streak & rewards → Weekly recap.`;
  return { html, text };
}
async function weeklyRecap(env, sendMail) {
  const wk = weekKey();
  const rows = (await env.DB.prepare(`SELECT g.user_id, g.stats, g.streak, g.tier, g.recap, u.email, u.name FROM game g JOIN users u ON u.id = g.user_id WHERE g.week_key = ? AND (g.recap_sent IS NULL OR g.recap_sent <> ?) AND ${PLUS_SQL}`).bind(wk, wk, Date.now() - GRACE, Date.now() - GRACE).all()).results;
  for (const r of rows) {
    const s = parse(r.stats, null); if (!s || s.wk !== wk || !(s.active > 0)) continue;
    await env.DB.prepare('UPDATE game SET recap_sent = ? WHERE user_id = ?').bind(wk, r.user_id).run();
    if (r.recap) await pushTo(env, r.user_id, { title: 'Your week in Self Streak 📊', body: `${s.active}/7 active days · ${s.xp} XP · ${s.habits || 0} habits · ${s.water || 0} glasses of water. Tap to see it all.`, tag: 'recap', url: './#/streak' });
    if (r.recap && sendMail) { try { const { html, text } = recapMail(shortName(r.name, r.user_id).split(' ')[0], s, r.streak, TIERS[r.tier] + ' league'); await sendMail(env, { to: r.email, subject: `Your week: ${s.active}/7 days, ${s.xp} XP 🔥`, html, text }); } catch (e) { console.error('recap mail', e); } }
  }
}
async function leagueRollover(env) {
  const wk = weekKey(), pw = addDay(wk, -7), since = addDay(istDay(), -21), moves = [];
  const all = (await env.DB.prepare(`SELECT user_id, tier, CASE WHEN week_key = ? THEN week_xp ELSE 0 END AS xp FROM game g WHERE board = 1 AND last_active >= ? AND EXISTS (SELECT 1 FROM users u WHERE u.id = g.user_id AND ${PLUS_SQL}) ORDER BY user_id`).bind(pw, since, Date.now() - GRACE, Date.now() - GRACE).all()).results;
  for (let tier = 0; tier < TIERS.length; tier++) {
    const rows = all.filter((r) => r.tier === tier);
    for (let s = 0; s < rows.length; s += GROUP) {
      const grp = rows.slice(s, s + GROUP).sort((a, b) => b.xp - a.xp || a.user_id.localeCompare(b.user_id)), n = grp.length;
      const up = tier < 4 ? Math.min(5, Math.max(1, Math.ceil(n / 4))) : 0, down = tier > 0 && n >= 8 ? Math.min(5, Math.floor(n / 4)) : 0;
      grp.forEach((r, k) => {
        let to = tier;
        if (k < up && r.xp > 0 && n >= 2) to = tier + 1; else if ((k >= n - down) || (tier > 0 && r.xp === 0)) to = Math.max(0, tier - 1);
        moves.push({ id: r.user_id, from: tier, to, rank: k + 1, of: n, xp: r.xp });
      });
    }
  }
  for (const m of moves) {
    await env.DB.prepare('UPDATE game SET tier = ?, result = ? WHERE user_id = ?').bind(m.to, JSON.stringify({ wk: pw, from: m.from, to: m.to, rank: m.rank, of: m.of, xp: m.xp }), m.id).run();
    if (m.to > m.from) await pushTo(env, m.id, { title: `You’re promoted to ${TIERS[m.to]} league! 🏆`, body: `You finished #${m.rank} last week with ${m.xp} XP.`, tag: 'league', url: './#/streak' });
  }
}
export async function gameCron(env, sendMail) {
  const now = Date.now(), d = new Date(now + IST), hm = d.getUTCHours() * 60 + d.getUTCMinutes(), t = istDay(), dow = d.getUTCDay();
  if (dow === 1 && hm < 120 && await once(env, 'league:' + weekKey())) await leagueRollover(env);
  if (hm >= 20 * 60 && hm < 21 * 60 && await once(env, 'risk:' + t)) await streakRisk(env, false);
  if (hm >= 22 * 60 + 30 && hm < 23 * 60 + 30 && await once(env, 'riskL:' + t)) await streakRisk(env, true);
  if (dow === 0 && hm >= 19 * 60 && hm < 22 * 60) await weeklyRecap(env, sendMail);
  if (hm < 10) await env.DB.prepare("DELETE FROM meta WHERE k LIKE 'nudge:%' AND CAST(v AS INTEGER) < ?").bind(now - 3 * DAY).run();
}

