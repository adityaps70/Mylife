// Runs before every `npm run deploy`. Stops a deploy that would put an out-of-date or unsaved copy live.
// Why: on 13–14 Nov 2026 the site was deployed from a copy that was missing commits on GitHub, and 11 pages
// (comparison pages, calculators, /about, Hindi pages) disappeared from selfstreak.com.
// Rule: what goes live = a commit that already contains everything on GitHub main.
// Emergency only: SKIP_DEPLOY_CHECK=1 npm run deploy
import { execSync } from 'node:child_process';
import { readFileSync, existsSync } from 'node:fs';

if (process.env.SKIP_DEPLOY_CHECK === '1') { console.log('Deploy check skipped (SKIP_DEPLOY_CHECK=1).'); process.exit(0); }
const sh = (c) => execSync(c, { encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'] }).trim();
const stop = (msg) => { console.error(`\n✋ Deploy stopped: ${msg}\n`); process.exit(1); };

// 1. Everything on GitHub main must be in this copy, or deploying would delete it from the live site.
try { sh('git fetch --quiet origin main'); } catch { stop('could not reach GitHub to check for newer changes. Check your connection and try again.'); }
const missing = sh('git rev-list --count HEAD..origin/main');
if (missing !== '0') stop(`GitHub main has ${missing} commit(s) this copy doesn't have (new pages, fixes). Run: git pull origin main   then deploy again.`);

// 2. Only committed work goes live, so GitHub always has a copy of what's on the site.
const dirty = sh('git status --porcelain --untracked-files=no -- src public scripts schema.sql wrangler.jsonc package.json');
if (dirty) stop(`these files have changes that aren't committed:\n${dirty}\nCommit them (git add -A && git commit -m "...") and deploy again. The deploy pushes to GitHub for you.`);

// 3. Every page in the sitemap must exist in this copy.
const sitemap = readFileSync(new URL('../public/sitemap.xml', import.meta.url), 'utf8');
const gone = [...sitemap.matchAll(/<loc>https:\/\/selfstreak\.com([^<]*)<\/loc>/g)].map((m) => m[1])
  .filter((p) => p !== '/' && !existsSync(new URL(`../public${p}.html`, import.meta.url)));
if (gone.length) stop(`pages listed in the sitemap are missing from public/: ${gone.join(', ')}`);

console.log('Deploy check passed: up to date with GitHub main, everything committed.');
