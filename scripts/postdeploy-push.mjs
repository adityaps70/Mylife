// Runs after a successful `npm run deploy`: commits the service-worker bump and IndexNow state, then pushes to
// GitHub main, so GitHub (and the daily SEO autopilot) always has exactly what is live.
import { execSync } from 'node:child_process';
const sh = (c) => execSync(c, { encoding: 'utf8', stdio: ['ignore', 'pipe', 'inherit'] }).trim();
sh('git add public/sw.js scripts/indexnow-state.json');
if (sh('git diff --cached --name-only')) sh('git commit -q -m "Deployed: bump service worker and IndexNow state"');
try { sh('git push -q origin HEAD:main'); console.log('Pushed to GitHub main.'); }
catch { console.error('Deployed, but the push to GitHub failed. Run: git pull origin main && git push origin HEAD:main'); process.exit(1); }
