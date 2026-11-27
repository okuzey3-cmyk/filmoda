const V="filmoda-v28";
const CORE=["./","index.html","manifest.webmanifest","icon-192.png","icon-512.png","tmdb-logo.png"];
self.addEventListener("install",e=>{e.waitUntil(caches.open(V).then(c=>c.addAll(CORE)));self.skipWaiting()});
self.addEventListener("activate",e=>{e.waitUntil(caches.keys().then(k=>Promise.all(k.filter(x=>x!==V).map(x=>caches.delete(x)))));self.clients.claim()});
self.addEventListener("fetch",e=>{
  const u=new URL(e.request.url);
  if(e.request.method!=="GET"||u.origin!==location.origin)return;
  e.respondWith(fetch(e.request,{cache:"no-cache"}).then(r=>{
    /* yalnizca saglam cevap saklanir; sunucu hata verirse eldeki saglam kopya kullanilir */
    if(r.ok){const c=r.clone();caches.open(V).then(x=>x.put(e.request,c));return r}
    return caches.match(e.request).then(m=>m||(e.request.mode==="navigate"?caches.match("index.html"):null)).then(m=>m||r)
  }).catch(()=>caches.match(e.request).then(m=>m||caches.match("index.html"))));
});
