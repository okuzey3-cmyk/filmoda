# Platform filtresi testi (tek seferlik): ekran goruntuleri + gercek filmlerin platformlari
import functools, http.server, os, socketserver, threading, json
from playwright.sync_api import sync_playwright
class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
srv = socketserver.TCPServer(("127.0.0.1", 8196), functools.partial(Q, directory="."))
threading.Thread(target=srv.serve_forever, daemon=True).start()
OUT="ai/plat"; os.makedirs(OUT, exist_ok=True); LOG=[]
def log(*a): print(*a, flush=True); LOG.append(" ".join(str(x) for x in a))
def snap(pg,n): pg.wait_for_timeout(500); pg.screenshot(path=f"{OUT}/{n}.png"); log("ok",n)
def gorsel(pg): pg.wait_for_function("(()=>{const a=[...document.querySelectorAll('#rail .card img')];return a.length>=1&&a.every(i=>i.complete&&i.naturalWidth>0)})()",timeout=40000); pg.wait_for_timeout(600)
def sec(pg):
    pg.evaluate("document.querySelectorAll('#moods .mood')[1].click()"); pg.wait_for_timeout(200)
    pg.evaluate("document.querySelectorAll('#sure .chip')[1].click()"); pg.wait_for_timeout(200)
    pg.evaluate("document.querySelectorAll('#kim .chip')[1].click()"); pg.wait_for_timeout(300)
with sync_playwright() as p:
    b=p.chromium.launch()
    c=b.new_context(viewport={"width":360,"height":640},device_scale_factor=3,is_mobile=True,has_touch=True,locale="tr-TR")
    pg=c.new_page(); errs=[]
    pg.on("pageerror",lambda e:errs.append(str(e)))
    urls=[]; pg.on("request",lambda r: urls.append(r.url) if "discover/movie" in r.url else None)
    pg.add_init_script("localStorage.setItem('filmoda_intro','1');sessionStorage.setItem('filmoda_acilis','1');")
    pg.goto("http://127.0.0.1:8196/index.html"); pg.wait_for_selector("#moods .mood",timeout=20000); pg.wait_for_timeout(900)
    snap(pg,"1-ana")
    pg.click("#plb"); pg.wait_for_timeout(600); snap(pg,"2-panel-bos")
    pg.evaluate("document.querySelector('.pfc .chip[data-id=\"8\"]').click()"); pg.wait_for_timeout(150)
    pg.evaluate("document.querySelector('.pfc .chip[data-id=\"337\"]').click()"); pg.wait_for_timeout(300); snap(pg,"3-panel-secili")
    pg.click("#pf-tm"); pg.wait_for_timeout(700); snap(pg,"4-ana-secili")
    log("pil:", pg.inner_text("#plt"))
    for run in range(3):
        if run==0: sec(pg)
        else:
            pg.evaluate("document.getElementById('back').click()"); pg.wait_for_timeout(500)
            pg.evaluate("document.querySelector('#go').click()")
        if run==0: pg.click("#go")
        pg.wait_for_selector("#rail .card",timeout=40000); gorsel(pg); pg.evaluate("window.scrollTo(0,0)")
        if run==0: snap(pg,"5-sonuc")
        n=pg.evaluate("document.querySelectorAll('#rail .card').length"); log("run",run,"kart",n)
        for i in range(n):
            pg.evaluate(f"document.querySelectorAll('#rail .card')[{i}].click()"); pg.wait_for_selector("#ad",timeout=40000); pg.wait_for_timeout(900)
            t=pg.inner_text("#sheet h2"); ab=pg.evaluate("[...document.querySelectorAll('#sheet .plat span.ab')].map(x=>x.textContent)")
            log("  film:",t,"| abonelik:",ab)
            pg.click("#cl"); pg.wait_for_timeout(500)
    # sonuc ekranindayken platformu degistir -> liste yenilenmeli
    pg.click("#plb"); pg.wait_for_timeout(500)
    pg.evaluate("document.querySelector('.pfc .chip[data-id=\"337\"]').click()"); pg.click("#pf-tm"); pg.wait_for_timeout(500)
    pg.wait_for_selector("#rail .card",timeout=40000); gorsel(pg); log("pil son:",pg.inner_text("#plt")); snap(pg,"6-sonuc-yenilendi")
    log("discover filtreli cagri sayisi:", sum(1 for u in urls if "with_watch_providers" in u), "/", len(urls))
    log("hatalar:",errs)
    b.close()
open(f"{OUT}/log.txt","w").write("\n".join(LOG))
