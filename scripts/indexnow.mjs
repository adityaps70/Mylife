// After a deploy, tell IndexNow (Bing, Yandex, Seznam, Naver…; Bing feeds ChatGPT search and Copilot)
// which URLs changed. Runs as part of `npm run deploy`.
//
// "Changed" = sitemap <lastmod> newer than the last successful ping (scripts/indexnow-state.json).
// First run, or `node scripts/indexnow.mjs --all`, sends every URL in the sitemap.
import { readFileSync, writeFileSync, existsSync } from 'node:fs';

const HOST = 'selfstreak.com';
const KEY = '51efd8f1dd95adbc4a9dd3e40e8ec21d';           // public/<KEY>.txt holds the same value
const sitemap = readFileSync(new URL('../public/sitemap.xml', import.meta.url), 'utf8');
const stateFile = new URL('./indexnow-state.json', import.meta.url);
const state = existsSync(stateFile) ? JSON.parse(readFileSync(stateFile, 'utf8')) : { lastPing: '' };

const entries = [...sitemap.matchAll(/<loc>([^<]+)<\/loc><lastmod>([^<]+)<\/lastmod>/g)].map(([, loc, lastmod]) => ({ loc, lastmod }));
const all = process.argv.includes('--all') || !state.lastPing;
const urls = entries.filter((e) => all || e.lastmod >= state.lastPing).map((e) => e.loc);

if (!urls.length) { console.log('IndexNow: nothing changed since', state.lastPing); process.exit(0); }

const res = await fetch('https://api.indexnow.org/indexnow', {
  method: 'POST',
  headers: { 'content-type': 'application/json; charset=utf-8' },
  body: JSON.stringify({ host: HOST, key: KEY, keyLocation: `https://${HOST}/${KEY}.txt`, urlList: urls }),
});
// 200 = accepted, 202 = accepted (key check pending). Anything else is an error worth seeing.
console.log(`IndexNow: ${res.status} for ${urls.length} URL(s)`);
if (res.status !== 200 && res.status !== 202) { console.log(await res.text()); process.exit(1); }
writeFileSync(stateFile, JSON.stringify({ lastPing: new Date().toISOString().slice(0, 10), sent: urls.length }, null, 1) + '\n');
