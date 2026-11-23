# Filmoda reklami icin gercek uygulama ekranlari (tek seferlik).
import functools, http.server, os, socketserver, threading
from playwright.sync_api import sync_playwright
class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
srv = socketserver.TCPServer(("127.0.0.1", 8197), functools.partial(Q, directory="."))
threading.Thread(target=srv.serve_forever, daemon=True).start()
OUT = "ai/sahne"; os.makedirs(OUT, exist_ok=True)
def hazir(pg, sel=None):
    pg.evaluate("document.fonts.ready")
    if sel: pg.wait_for_function("(s)=>{const a=[...document.querySelectorAll(s)];return a.length>=2&&a.every(i=>i.complete&&i.naturalWidth>0)}", arg=sel, timeout=40000)
    pg.wait_for_timeout(700)
def snap(pg, n): pg.screenshot(path=f"{OUT}/{n}.png"); print("ok", n, flush=True)
with sync_playwright() as p:
    b = p.chromium.launch()
    c = b.new_context(viewport={"width": 360, "height": 640}, device_scale_factor=3, is_mobile=True, has_touch=True, locale="tr-TR")
    pg = c.new_page(); pg.add_init_script("localStorage.setItem('filmoda_intro','1');")
    pg.goto("http://127.0.0.1:8197/index.html"); pg.wait_for_selector("#moods .mood", timeout=20000); pg.wait_for_timeout(900)
    snap(pg, "ana")
    pg.evaluate("document.querySelectorAll('#moods .mood')[1].click()"); pg.wait_for_timeout(500); snap(pg, "ruh")
    pg.evaluate("document.querySelectorAll('#sure button, #sure .chip')[1].click()"); pg.wait_for_timeout(300)
    pg.evaluate("document.querySelectorAll('#kim button, #kim .chip')[1].click()"); pg.wait_for_timeout(500)
    pg.evaluate("var e=document.getElementById('sure').previousElementSibling;window.scrollTo(0,e.getBoundingClientRect().top+window.scrollY-24)"); pg.wait_for_timeout(500)
    snap(pg, "secim")
    pg.click("#go"); pg.wait_for_selector("#rail .card", timeout=40000); hazir(pg, "#rail .card img")
    pg.evaluate("window.scrollTo(0,0)"); pg.wait_for_timeout(300)
    n = pg.evaluate("document.querySelectorAll('#rail .card').length")
    for i in range(min(3, n)):
        pg.evaluate(f"document.querySelectorAll('#rail .card')[{i}].scrollIntoView({{inline:'center',block:'nearest',behavior:'instant'}})"); pg.wait_for_timeout(600)
        snap(pg, f"sonuc{i+1}")
        pg.locator("#rail .card").nth(i).screenshot(path=f"{OUT}/kart{i+1}.png"); print("kart", i+1, flush=True)
    pg.evaluate("document.querySelectorAll('#rail .card')[0].scrollIntoView({inline:'center',block:'nearest',behavior:'instant'})"); pg.wait_for_timeout(300)
    pg.evaluate("document.querySelectorAll('#rail .card')[0].click()"); pg.wait_for_selector("#ad", timeout=40000); pg.wait_for_timeout(1500)
    snap(pg, "detay")
    pg.evaluate("document.getElementById('sheet').scrollTo({top:330,behavior:'instant'})"); pg.wait_for_timeout(600); snap(pg, "detay2")
    b.close()
