-- Self Streak database (Cloudflare D1)
CREATE TABLE IF NOT EXISTS users (
  id TEXT PRIMARY KEY,
  email TEXT NOT NULL UNIQUE,
  name TEXT NOT NULL DEFAULT '',
  pass_hash TEXT NOT NULL,
  salt TEXT NOT NULL,
  plan TEXT NOT NULL DEFAULT 'trial',          -- trial | active | owner | cancelled
  trial_ends INTEGER NOT NULL,                -- ms epoch
  paid_until INTEGER NOT NULL DEFAULT 0,      -- ms epoch, set by the payment webhook later
  fail_count INTEGER NOT NULL DEFAULT 0,
  locked_until INTEGER NOT NULL DEFAULT 0,
  created INTEGER NOT NULL
);
CREATE TABLE IF NOT EXISTS sessions (
  token_hash TEXT PRIMARY KEY,
  user_id TEXT NOT NULL,
  expires INTEGER NOT NULL
);
CREATE INDEX IF NOT EXISTS sessions_user ON sessions(user_id);
CREATE TABLE IF NOT EXISTS user_data (
  user_id TEXT PRIMARY KEY,
  json TEXT NOT NULL,
  updated INTEGER NOT NULL
);
CREATE TABLE IF NOT EXISTS usage (
  user_id TEXT NOT NULL,
  day TEXT NOT NULL,                          -- YYYY-MM-DD in India time
  count INTEGER NOT NULL DEFAULT 0,
  PRIMARY KEY (user_id, day)
);
CREATE TABLE IF NOT EXISTS push_subs (
  endpoint TEXT PRIMARY KEY,
  user_id TEXT NOT NULL,
  p256dh TEXT NOT NULL,
  auth TEXT NOT NULL,
  created INTEGER NOT NULL
);
CREATE INDEX IF NOT EXISTS push_subs_user ON push_subs(user_id);
CREATE TABLE IF NOT EXISTS push_schedule (
  user_id TEXT PRIMARY KEY,
  items TEXT NOT NULL,                        -- JSON [{at,title,body,url,tag,actions,acts}]
  last_sent INTEGER NOT NULL DEFAULT 0,
  updated INTEGER NOT NULL
);
CREATE TABLE IF NOT EXISTS payments (
  order_id TEXT PRIMARY KEY,
  user_id TEXT NOT NULL,
  amount INTEGER NOT NULL,
  status TEXT NOT NULL,          -- created | paid | expired | terminated
  created INTEGER NOT NULL,
  paid_at INTEGER
);
CREATE INDEX IF NOT EXISTS payments_user ON payments(user_id);
CREATE TABLE IF NOT EXISTS password_resets (
  token_hash TEXT PRIMARY KEY,
  user_id TEXT NOT NULL,
  expires INTEGER NOT NULL,
  used INTEGER NOT NULL DEFAULT 0,
  created INTEGER NOT NULL
);
CREATE INDEX IF NOT EXISTS password_resets_user ON password_resets(user_id, created);
-- Analytics (privacy-friendly: no cookies, no IPs stored)
ALTER TABLE users ADD COLUMN last_seen INTEGER NOT NULL DEFAULT 0;
CREATE TABLE IF NOT EXISTS active_days (user_id TEXT NOT NULL, day TEXT NOT NULL, PRIMARY KEY (user_id, day));
CREATE TABLE IF NOT EXISTS page_views (day TEXT NOT NULL, path TEXT NOT NULL, ref TEXT NOT NULL, country TEXT NOT NULL, device TEXT NOT NULL, n INTEGER NOT NULL DEFAULT 0, PRIMARY KEY (day, path, ref, country, device));
CREATE TABLE IF NOT EXISTS visitors (day TEXT NOT NULL, h TEXT NOT NULL, PRIMARY KEY (day, h));
-- Streaks, leagues, friends and referrals
CREATE TABLE IF NOT EXISTS game (
  user_id TEXT PRIMARY KEY, code TEXT NOT NULL UNIQUE, ref_by TEXT,
  streak INTEGER NOT NULL DEFAULT 0, best INTEGER NOT NULL DEFAULT 0, last_active TEXT, days TEXT NOT NULL DEFAULT '[]',
  xp INTEGER NOT NULL DEFAULT 0, week_key TEXT, week_xp INTEGER NOT NULL DEFAULT 0, tier INTEGER NOT NULL DEFAULT 0, freezes INTEGER NOT NULL DEFAULT 0,
  board INTEGER NOT NULL DEFAULT 1, recap INTEGER NOT NULL DEFAULT 1, risk INTEGER NOT NULL DEFAULT 1,
  stats TEXT, result TEXT, risk_sent TEXT, recap_sent TEXT, updated INTEGER NOT NULL DEFAULT 0
);
CREATE INDEX IF NOT EXISTS game_tier ON game(tier, board);
CREATE INDEX IF NOT EXISTS game_ref ON game(ref_by);
CREATE TABLE IF NOT EXISTS friends (a TEXT NOT NULL, b TEXT NOT NULL, created INTEGER NOT NULL, PRIMARY KEY (a, b));
CREATE TABLE IF NOT EXISTS meta (k TEXT PRIMARY KEY, v TEXT);

-- Sign in with Apple: Apple user ID (sub) → account. Also created on first use by the worker.
CREATE TABLE IF NOT EXISTS apple_ids (sub TEXT PRIMARY KEY, user_id TEXT NOT NULL, created INTEGER NOT NULL);
