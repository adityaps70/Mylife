// Apple App Store + Google Play subscriptions for Self Streak Plus inside the iOS / Android apps.
// The app buys through StoreKit / Play Billing, then sends us the transaction; we confirm it with Apple / Google
// directly (never trusting the phone) and extend paid_until. Renewals are picked up lazily: when a store
// subscriber's access is about to run out, /api/me asks the store again.
// State lives in the `meta` table:
//   store:<userId>             -> JSON { platform, product, ref, expires, state, checked }
//   storeref:<platform>:<ref>  -> userId   (one store subscription can unlock only one Self Streak account)
//
// Secrets (set with `npx wrangler secret put …`):
//   APPLE_IAP_KEY_ID, APPLE_IAP_ISSUER_ID, APPLE_IAP_PRIVATE_KEY  (App Store Connect → Users and Access → Integrations → In-App Purchase key, .p8 contents)
//   GOOGLE_PLAY_SA_JSON                                            (Google Cloud service account JSON with access in Play Console)
// Vars: STORE_PRODUCT_ID (default plus_monthly), PLAY_BASE_PLAN (default monthly), APP_BUNDLE_ID (default com.selfstreak.app)
const DAY = 86400000;
const te = new TextEncoder();
const json = (d, status = 200) => new Response(JSON.stringify(d), { status, headers: { 'content-type': 'application/json', 'cache-control': 'no-store' } });
const err = (status, error) => json({ error }, status);
const getMeta = async (env, k) => (await env.DB.prepare('SELECT v FROM meta WHERE k = ?').bind(k).first())?.v ?? null;
const setMeta = (env, k, v) => env.DB.prepare('INSERT INTO meta (k, v) VALUES (?, ?) ON CONFLICT(k) DO UPDATE SET v = excluded.v').bind(k, v).run();

const b64url = (buf) => btoa(String.fromCharCode(...new Uint8Array(buf))).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
const b64urlStr = (s) => b64url(te.encode(s));
const unb64url = (s) => { s = s.replace(/-/g, '+').replace(/_/g, '/'); while (s.length % 4) s += '='; return atob(s); };
const jwsPayload = (jws) => { try { return JSON.parse(decodeURIComponent(escape(unb64url(String(jws).split('.')[1])))); } catch { return null; } };
const pemBytes = (pem) => Uint8Array.from(atob(String(pem).replace(/-----[^-]+-----/g, '').replace(/\\n/g, '').replace(/\s+/g, '')), (c) => c.charCodeAt(0));

export function storeCfg(env) {
  return {
    apple: !!(env.APPLE_IAP_KEY_ID && env.APPLE_IAP_ISSUER_ID && env.APPLE_IAP_PRIVATE_KEY),
    google: !!env.GOOGLE_PLAY_SA_JSON,
    product: env.STORE_PRODUCT_ID || 'plus_monthly',
    basePlan: env.PLAY_BASE_PLAN || 'monthly',
    bundle: env.APP_BUNDLE_ID || 'com.selfstreak.app',
  };
}
export async function storeSubOf(env, uid) { const v = await getMeta(env, 'store:' + uid); try { return v ? JSON.parse(v) : null; } catch { return null; } }

/* ---------- Apple: App Store Server API (signed with our In-App Purchase key) ---------- */
let appleKey = null;
async function appleJWT(env, C) {
  if (!appleKey) appleKey = await crypto.subtle.importKey('pkcs8', pemBytes(env.APPLE_IAP_PRIVATE_KEY), { name: 'ECDSA', namedCurve: 'P-256' }, false, ['sign']);
  const now = Math.floor(Date.now() / 1000);
  const head = b64urlStr(JSON.stringify({ alg: 'ES256', kid: env.APPLE_IAP_KEY_ID, typ: 'JWT' }));
  const body = b64urlStr(JSON.stringify({ iss: env.APPLE_IAP_ISSUER_ID, iat: now, exp: now + 1200, aud: 'appstoreconnect-v1', bid: C.bundle }));
  const sig = await crypto.subtle.sign({ name: 'ECDSA', hash: 'SHA-256' }, appleKey, te.encode(head + '.' + body));
  return head + '.' + body + '.' + b64url(sig);
}
async function appleGet(env, C, path) {
  const auth = 'Bearer ' + (await appleJWT(env, C));
  for (const host of ['https://api.storekit.itunes.apple.com', 'https://api.storekit-sandbox.itunes.apple.com']) {
    const r = await fetch(host + path, { headers: { authorization: auth } });
    if (r.status === 404) continue; // not in this environment: try sandbox (TestFlight / review)
    const d = await r.json().catch(() => ({}));
    if (!r.ok) { console.error('appstore', path, r.status, JSON.stringify(d).slice(0, 300)); const e = new Error('Couldn’t confirm the purchase with Apple. Try again in a minute.'); e.status = 502; throw e; }
    return d;
  }
  const e = new Error('Apple doesn’t know this purchase.'); e.status = 404; throw e;
}
// Ask Apple for the subscription's current state. `id` can be any transaction id of the subscription.
async function appleCheck(env, C, id, uid) {
  const d = await appleGet(env, C, '/inApps/v1/subscriptions/' + encodeURIComponent(id));
  let best = null;
  for (const g of d.data || []) for (const lt of g.lastTransactions || []) {
    const t = jwsPayload(lt.signedTransactionInfo), rn = jwsPayload(lt.signedRenewalInfo) || {};
    if (!t || t.bundleId !== C.bundle || t.productId !== C.product) continue;
    const entitled = (lt.status === 1 || lt.status === 4) && !t.revocationDate; // 1 active, 4 billing grace period
    const expires = Math.max(Number(t.expiresDate) || 0, lt.status === 4 ? Number(rn.gracePeriodExpiresDate) || 0 : 0);
    const rec = { platform: 'ios', product: t.productId, ref: String(t.originalTransactionId), expires, state: entitled ? (rn.autoRenewStatus === 0 ? 'cancelling' : 'active') : 'ended', owner: t.appAccountToken || null, env: t.environment };
    if (!best || rec.expires > best.expires) best = rec;
  }
  if (!best) { const e = new Error('This purchase isn’t a Self Streak Plus subscription.'); e.status = 400; throw e; }
  if (best.owner && uid && best.owner.toLowerCase() !== uid.toLowerCase()) { const e = new Error('This App Store subscription belongs to another Self Streak account.'); e.status = 409; throw e; }
  return best;
}

/* ---------- Google: Play Developer API (service-account OAuth) ---------- */
let gTok = null;
async function googleToken(env) {
  if (gTok && gTok.exp > Date.now() + 60e3) return gTok.v;
  const sa = JSON.parse(env.GOOGLE_PLAY_SA_JSON), now = Math.floor(Date.now() / 1000);
  const key = await crypto.subtle.importKey('pkcs8', pemBytes(sa.private_key), { name: 'RSASSA-PKCS1-v1_5', hash: 'SHA-256' }, false, ['sign']);
  const unsigned = b64urlStr(JSON.stringify({ alg: 'RS256', typ: 'JWT' })) + '.' + b64urlStr(JSON.stringify({ iss: sa.client_email, scope: 'https://www.googleapis.com/auth/androidpublisher', aud: 'https://oauth2.googleapis.com/token', iat: now, exp: now + 3600 }));
  const jwt = unsigned + '.' + b64url(await crypto.subtle.sign('RSASSA-PKCS1-v1_5', key, te.encode(unsigned)));
  const r = await fetch('https://oauth2.googleapis.com/token', { method: 'POST', headers: { 'content-type': 'application/x-www-form-urlencoded' }, body: 'grant_type=urn%3Aietf%3Aparams%3Aoauth%3Agrant-type%3Ajwt-bearer&assertion=' + jwt });
  const d = await r.json().catch(() => ({}));
  if (!r.ok || !d.access_token) { console.error('play token', r.status, JSON.stringify(d).slice(0, 300)); const e = new Error('Couldn’t reach Google Play. Try again in a minute.'); e.status = 502; throw e; }
  gTok = { v: d.access_token, exp: Date.now() + (d.expires_in || 3600) * 1000 };
  return gTok.v;
}
async function googleCheck(env, C, token, uid) {
  const base = 'https://androidpublisher.googleapis.com/androidpublisher/v3/applications/' + encodeURIComponent(C.bundle) + '/purchases/';
  const auth = { authorization: 'Bearer ' + (await googleToken(env)) };
  const r = await fetch(base + 'subscriptionsv2/tokens/' + encodeURIComponent(token), { headers: auth });
  const d = await r.json().catch(() => ({}));
  if (!r.ok) { console.error('play sub', r.status, JSON.stringify(d).slice(0, 300)); const e = new Error(r.status === 404 || r.status === 400 ? 'Google Play doesn’t know this purchase.' : 'Couldn’t confirm the purchase with Google Play. Try again in a minute.'); e.status = r.status === 404 || r.status === 400 ? 400 : 502; throw e; }
  const li = (d.lineItems || []).find((x) => x.productId === C.product);
  if (!li) { const e = new Error('This purchase isn’t a Self Streak Plus subscription.'); e.status = 400; throw e; }
  const owner = d.externalAccountIdentifiers?.obfuscatedExternalAccountId || null;
  if (owner && uid && owner.toLowerCase() !== uid.toLowerCase()) { const e = new Error('This Google Play subscription belongs to another Self Streak account.'); e.status = 409; throw e; }
  const st = d.subscriptionState || '', entitled = ['SUBSCRIPTION_STATE_ACTIVE', 'SUBSCRIPTION_STATE_IN_GRACE_PERIOD', 'SUBSCRIPTION_STATE_CANCELED'].includes(st);
  const expires = Date.parse(li.expiryTime) || 0;
  // Purchases must be acknowledged within 3 days or Google refunds them (the app also does this; this is the safety net).
  if (d.acknowledgementState === 'ACKNOWLEDGEMENT_STATE_PENDING' && entitled) await fetch(base + 'subscriptions/' + encodeURIComponent(C.product) + '/tokens/' + encodeURIComponent(token) + ':acknowledge', { method: 'POST', headers: { ...auth, 'content-type': 'application/json' }, body: '{}' }).catch(() => {});
  return { platform: 'android', product: li.productId, ref: token, expires, state: entitled && expires > Date.now() ? (st === 'SUBSCRIPTION_STATE_CANCELED' ? 'cancelling' : 'active') : 'ended', owner, linked: d.linkedPurchaseToken || null };
}

/* ---------- shared ---------- */
async function apply(env, uid, rec) {
  const prevOwner = await getMeta(env, 'storeref:' + rec.platform + ':' + rec.ref);
  if (prevOwner && prevOwner !== uid) { const e = new Error(`This ${rec.platform === 'ios' ? 'App Store' : 'Google Play'} subscription is already linked to another Self Streak account.`); e.status = 409; throw e; }
  const saved = { platform: rec.platform, product: rec.product, ref: rec.ref, expires: rec.expires, state: rec.state, checked: Date.now() };
  await setMeta(env, 'store:' + uid, JSON.stringify(saved));
  await setMeta(env, 'storeref:' + rec.platform + ':' + rec.ref, uid);
  if (rec.state !== 'ended' && rec.expires > Date.now())
    await env.DB.prepare("UPDATE users SET paid_until = MAX(paid_until, ?), plan = CASE WHEN plan = 'owner' THEN plan ELSE 'active' END WHERE id = ?").bind(rec.expires, uid).run();
  return saved;
}
const check = (env, C, platform, ref, uid) => (platform === 'ios' ? appleCheck(env, C, ref, uid) : googleCheck(env, C, ref, uid));

// POST /api/billing/store/verify { platform: 'ios'|'android', transactionId?, purchaseToken? }
export async function storeRoutes(req, env, p, m, body, u) {
  if (p !== '/api/billing/store/verify' || m !== 'POST') return null;
  const C = storeCfg(env), platform = body?.platform === 'android' ? 'android' : body?.platform === 'ios' ? 'ios' : null;
  if (!platform) return err(400, 'Unknown store.');
  if (platform === 'ios' && !C.apple) return err(503, 'App Store purchases aren’t switched on yet.');
  if (platform === 'android' && !C.google) return err(503, 'Google Play purchases aren’t switched on yet.');
  const ref = String((platform === 'ios' ? body.transactionId : body.purchaseToken) || '').slice(0, 2000);
  if (!ref) return err(400, 'Missing purchase details.');
  try {
    const rec = await check(env, C, platform, ref, u.id);
    const saved = await apply(env, u.id, rec);
    return json({ ok: true, store: saved, active: saved.state !== 'ended' && saved.expires > Date.now() });
  } catch (e) { return err(e.status || 500, e.message || 'Couldn’t confirm the purchase.'); }
}

// Called before /api/me: when a store subscriber's access is close to ending, ask the store whether it renewed.
export async function storeRefresh(env, u) {
  if (u.paid_until > Date.now() + 2 * 3600e3) return false;
  const s = await storeSubOf(env, u.id); if (!s || s.state === 'ended' && s.expires < Date.now() - 30 * DAY) return false;
  if (Date.now() - (s.checked || 0) < 6 * 3600e3) return false;
  const C = storeCfg(env); if ((s.platform === 'ios' && !C.apple) || (s.platform === 'android' && !C.google)) return false;
  try {
    const rec = await check(env, C, s.platform, s.ref, u.id); const saved = await apply(env, u.id, rec);
    if (saved.state !== 'ended' && saved.expires > u.paid_until) { u.paid_until = saved.expires; if (u.plan !== 'owner') u.plan = 'active'; }
    return true;
  } catch (e) { await setMeta(env, 'store:' + u.id, JSON.stringify({ ...s, checked: Date.now() })); console.error('store refresh', e.message); return false; }
}
