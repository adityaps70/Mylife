// Give every deploy a new service-worker cache name so installed apps update themselves.
import { readFileSync, writeFileSync } from 'node:fs';
const p = new URL('../public/sw.js', import.meta.url);
const s = readFileSync(p, 'utf8').replace(/const CACHE='[^']*'/, `const CACHE='selfstreak-${Date.now().toString(36)}'`);
writeFileSync(p, s);
console.log('sw cache bumped');
