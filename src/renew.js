// Renewal reminders: push + email 3 days before, 1 day before and on the day Plus/trial ends,
// and once more when the 3-day grace period is over and Plus features lock.
// Skipped for owners and for people whose Razorpay autopay is on (Razorpay notifies them itself).
import { sendPush } from './webpush.js';
import { autopayOf } from './razorpay.js';

const DAY = 86400000, IST = 5.5 * 3600e3, GRACE = 3 * DAY;
const istDay = (t) => new Date(t + IST).toISOString().slice(0, 10);
const dayDiff = (a, b) => Math.round((Date.parse(istDay(b)) - Date.parse(istDay(a))) / DAY);
const esc = (s) => String(s ?? '').replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const fmt = (t) => new Date(t + IST).toLocaleDateString('en-IN', { day: 'numeric', month: 'short', timeZone: 'UTC' });

function message(tag, trial, price, end) {
  const what = trial ? 'Your free trial' : 'Self Streak Plus';
  const keep = `Renew for ₹${price}/month to keep AI logging, photo scans, reminders and leagues.`;
  switch (tag) {
    case 'd3': return { title: `${what} ends in 3 days`, body: `${keep} Your streak and data stay safe either way.` };
    case 'd1': return { title: `${what} ends tomorrow`, body: `${keep} Autopay takes 30 seconds to set up.` };
    case 'd0': return { title: `${what} ends today`, body: `You get 3 extra days with everything on, then Plus features lock on ${fmt(end + GRACE)}. ${keep}` };
    case 'locked': return { title: 'Plus features are now locked', body: `You're on the Free plan: habits, water, expenses and your streak still work. Renew anytime for ₹${price}/month to unlock AI logging, scans and reminders.` };
  }
  return null;
}
function mail(name, msg) {
  const html = `<div style="font-family:system-ui,sans-serif;background:#09090b;color:#f4f4f5;padding:28px"><div style="max-width:480px;margin:auto;background:#141418;border:1px solid #26262c;border-radius:20px;padding:28px">
  <div style="font-size:13px;color:#a1a1aa;letter-spacing:.06em">SELF STREAK</div><h1 style="font-size:24px;margin:8px 0 10px">${esc(msg.title)}</h1>
  <p style="color:#d4d4d8;line-height:1.55;margin:0 0 20px">Hi ${esc(name || 'there')}, ${esc(msg.body)}</p>
  <a href="https://selfstreak.com/app#/settings?renew" style="display:block;text-align:center;background:#d7f64a;color:#10120a;font-weight:800;padding:14px;border-radius:999px;text-decoration:none">Renew Self Streak Plus →</a>
  <p style="font-size:12px;color:#71717a;margin-top:18px">You get this because your Self Streak plan is ending. Questions? Reply or email adityaps700@gmail.com.</p></div></div>`;
  return { html, text: `${msg.title}\n\n${msg.body}\n\nRenew: https://selfstreak.com/app#/settings?renew` };
}

export async function renewalReminders(env, sendMail) {
  const now = Date.now(), price = Number(env.PRICE_INR || 199);
  const rows = (await env.DB.prepare(`SELECT id, email, name, paid_until, trial_ends FROM users WHERE plan <> 'owner'
      AND MAX(paid_until, trial_ends) BETWEEN ? AND ?`).bind(now - 5 * DAY, now + 4 * DAY).all()).results;
  for (const u of rows) {
    const end = Math.max(u.paid_until || 0, u.trial_ends || 0), dd = dayDiff(now, end);
    const tag = dd === 3 ? 'd3' : dd === 1 ? 'd1' : dd === 0 ? 'd0' : dd === -3 ? 'locked' : null;
    if (!tag) continue;
    const ap = await autopayOf(env, u.id).catch(() => null);
    if (ap && ['active', 'authenticated'].includes(ap.status) && !ap.cancelling) continue;
    const key = `renew:${u.id}:${tag}:${istDay(end)}`;
    const ins = await env.DB.prepare('INSERT OR IGNORE INTO meta (k, v) VALUES (?, ?)').bind(key, String(now)).run();
    if (!ins.meta.changes) continue;
    const msg = message(tag, !(u.paid_until > 0), price, end);
    const subs = (await env.DB.prepare('SELECT * FROM push_subs WHERE user_id = ?').bind(u.id).all()).results;
    for (const s of subs) { try { const st = await sendPush(s, { ...msg, tag: 'renew', url: './#/settings?renew' }, env); if (st === 404 || st === 410) await env.DB.prepare('DELETE FROM push_subs WHERE endpoint = ?').bind(s.endpoint).run(); } catch (e) {} }
    if (sendMail) { try { const { html, text } = mail(String(u.name || '').split(' ')[0], msg); await sendMail(env, { to: u.email, subject: msg.title, html, text }); } catch (e) { console.error('renew mail', e); } }
  }
}
