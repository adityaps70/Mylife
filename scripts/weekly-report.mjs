// Weekly traffic + signup report from the live D1 database (read-only queries).
//   node scripts/weekly-report.mjs            -> last 7 days vs the 7 before, printed and saved to seo/reports/traffic-<date>.md
// Page views come from the /api/hit beacon on public pages (bots skipped, no cookies; visitors = daily one-way hash).
import { execFileSync } from 'node:child_process';
import { writeFileSync } from 'node:fs';

const q = (sql) => JSON.parse(execFileSync('npx', ['wrangler', 'd1', 'execute', 'self-streak', '--remote', '--json', '--command', sql], { encoding: 'utf8', stdio: ['ignore', 'pipe', 'ignore'] }))[0].results;
const ist = (d) => new Date(d.getTime() + 5.5 * 3600e3).toISOString().slice(0, 10);
const now = new Date(), day = 864e5;
const from = ist(new Date(now - 7 * day)), prev = ist(new Date(now - 14 * day)), today = ist(now);
const ms = (s) => Date.parse(s + 'T00:00:00+05:30');

const views = (a, b) => q(`SELECT COALESCE(SUM(n),0) AS n FROM page_views WHERE day > '${a}' AND day <= '${b}'`)[0].n;
const visitors = (a, b) => q(`SELECT COUNT(*) AS n FROM visitors WHERE day > '${a}' AND day <= '${b}'`)[0].n;
const signups = (a, b) => q(`SELECT COUNT(*) AS n FROM users WHERE created > ${ms(a) + day} AND created <= ${ms(b) + day}`)[0].n;
const paid = (a, b) => q(`SELECT COUNT(*) AS n FROM payments WHERE status = 'paid' AND paid_at > ${ms(a) + day} AND paid_at <= ${ms(b) + day}`)[0].n;
const pct = (a, b) => (b ? `${a >= b ? '+' : ''}${Math.round((a - b) / b * 100)}%` : 'new');

const cur = { v: views(from, today), u: visitors(from, today), s: signups(from, today), p: paid(from, today) };
const old = { v: views(prev, from), u: visitors(prev, from), s: signups(prev, from), p: paid(prev, from) };
const top = q(`SELECT path, SUM(n) AS n FROM page_views WHERE day > '${from}' GROUP BY path ORDER BY n DESC LIMIT 15`);
const refs = q(`SELECT CASE ref WHEN '' THEN '(direct / internal)' ELSE ref END AS ref, SUM(n) AS n FROM page_views WHERE day > '${from}' GROUP BY ref ORDER BY n DESC LIMIT 10`);
const dev = q(`SELECT device, SUM(n) AS n FROM page_views WHERE day > '${from}' GROUP BY device ORDER BY n DESC`);
const geo = q(`SELECT country, SUM(n) AS n FROM page_views WHERE day > '${from}' GROUP BY country ORDER BY n DESC LIMIT 5`);

const t = (rows, a, b) => rows.map((r) => `| ${r[a] || '?'} | ${r[b]} |`).join('\n');
const md = `# Traffic report, ${from} to ${today} (IST)

| | Last 7 days | 7 days before | Change |
|---|---|---|---|
| Page views (public pages) | ${cur.v} | ${old.v} | ${pct(cur.v, old.v)} |
| Unique visitors | ${cur.u} | ${old.u} | ${pct(cur.u, old.u)} |
| Sign-ups | ${cur.s} | ${old.s} | ${pct(cur.s, old.s)} |
| Paid payments | ${cur.p} | ${old.p} | ${pct(cur.p, old.p)} |
| Sign-ups per 100 visitors | ${cur.u ? (cur.s / cur.u * 100).toFixed(1) : '–'} | ${old.u ? (old.s / old.u * 100).toFixed(1) : '–'} | |

## Top pages
| Path | Views |
|---|---|
${t(top, 'path', 'n')}

## Referrers
| Source | Views |
|---|---|
${t(refs, 'ref', 'n')}

## Devices
| Device | Views |
|---|---|
${t(dev, 'device', 'n')}

## Countries
| Country | Views |
|---|---|
${t(geo, 'country', 'n')}
`;
writeFileSync(new URL(`../seo/reports/traffic-${today}.md`, import.meta.url), md);
console.log(md);
