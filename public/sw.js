/* Aditya OS service worker: offline app shell + reminder notifications */
const CACHE='selfstreak-v11101914';
const SHELL=['./manifest.webmanifest','./icon-192.png','./icon-512.png'];
self.addEventListener('install',e=>{e.waitUntil(caches.open(CACHE).then(c=>Promise.all([c.addAll(SHELL).catch(()=>{}),fetch('./app').then(r=>r.ok&&c.put('./index.html',r)).catch(()=>{})])).then(()=>self.skipWaiting()))});
self.addEventListener('activate',e=>{e.waitUntil(caches.keys().then(ks=>Promise.all(ks.filter(k=>k!==CACHE&&k!=='nudges').map(k=>caches.delete(k)))).then(()=>self.clients.claim()))});
self.addEventListener('fetch',e=>{
  const req=e.request,u=new URL(req.url);
  if(req.method!=='GET'||u.origin!==location.origin)return;
  // Pages: network first so updates arrive, cached copy when offline.
  if(req.mode==='navigate'){if(/^\/(terms|privacy|refunds|contact|landing)/.test(u.pathname))return;e.respondWith(fetch(req).then(r=>{if(r.ok&&!r.headers.get('x-ss-page')&&!r.redirected){const cp=r.clone();caches.open(CACHE).then(c=>c.put('./index.html',cp))}return r}).catch(()=>caches.match('./index.html').then(r=>r||caches.match('./'))));return}
  e.respondWith(caches.match(req).then(r=>r||fetch(req)));
});
async function showDue(){
  const c=await caches.open('nudges'),r=await c.match('schedule.json');if(!r)return;
  const s=await r.json(),lr=await c.match('lastrun'),last=lr?+(await lr.text()):Date.now()-3600e3,now=Date.now();
  const due=(s.items||[]).filter(i=>i.at>last&&i.at<=now&&i.at>now-3*3600e3);
  for(const it of due.slice(-4))await self.registration.showNotification(it.title,{body:it.body,tag:it.tag,icon:'icon-192.png',badge:'icon-192.png',data:{url:it.url,acts:it.acts},actions:it.actions||[]});
  await c.put('lastrun',new Response(String(now)));
}
self.addEventListener('periodicsync',e=>{if(e.tag==='nudges')e.waitUntil(showDue())});
self.addEventListener('message',e=>{if(e.data&&e.data.type==='check')e.waitUntil(showDue())});
// Ready for a future push server: shows whatever it sends.
self.addEventListener('push',e=>{let d={};try{d=e.data.json()}catch(x){d={title:'Reminder',body:e.data?e.data.text():''}}
  e.waitUntil(self.registration.showNotification(d.title||'Reminder',{body:d.body||'',tag:d.tag,icon:'icon-192.png',badge:'icon-192.png',data:{url:d.url||'./',acts:d.acts||{}},actions:d.actions||[]}))});
self.addEventListener('notificationclick',e=>{
  e.notification.close();
  const d=e.notification.data||{},act=e.action&&d.acts?d.acts[e.action]:null,url=new URL(d.url||'./',self.registration.scope);
  if(act)url.searchParams.set('do',act);
  e.waitUntil(self.clients.matchAll({type:'window',includeUncontrolled:true}).then(cs=>{
    const q=act||url.searchParams.get('do');
    for(const c of cs){if('focus' in c){if(q)c.postMessage({type:'notif-action',act:q});else if(url.hash)c.navigate?.(url.href);return c.focus()}}
    return self.clients.openWindow(url.href);
  }));
});
