# Filmoda: Play Store icin GERCEK ekran goruntuleri (tek seferlik, elle tetiklenir).
import functools, http.server, os, socketserver, threading
from playwright.sync_api import sync_playwright
class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
srv = socketserver.TCPServer(("127.0.0.1", 8199), functools.partial(Q, directory="."))
threading.Thread(target=srv.serve_forever, daemon=True).start()
OUT = "ai/ekranlar"; os.makedirs(OUT, exist_ok=True)
def bekle_gorseller(pg):
    pg.wait_for_function("[...document.images].every(i=>i.complete)", timeout=30000)
    pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(700)
def snap(pg, n):
    bekle_gorseller(pg); pg.screenshot(path=f"{OUT}/ekran-{n}.png"); print("ok", n)
with sync_playwright() as p:
    b = p.chromium.launch()
    c = b.new_context(viewport={"width": 360, "height": 640}, device_scale_factor=3, is_mobile=True, has_touch=True, locale="tr-TR")
    pg = c.new_page()
    pg.add_init_script("localStorage.setItem('filmoda_intro','1');")
    pg.goto("http://127.0.0.1:8199/index.html"); pg.wait_for_selector("#moods .mood", timeout=20000); pg.wait_for_timeout(800)
    snap(pg, 1)                                   # ana ekran
    pg.evaluate("document.querySelectorAll('#moods .mood')[1].click()"); pg.wait_for_timeout(500)
    snap(pg, 2)                                   # ruh hali secildi (sure/kimlesin)
    pg.click("#go"); pg.wait_for_selector("#rail .card", timeout=40000); pg.wait_for_timeout(600)
    snap(pg, 3)                                   # sonuc kartlari
    n = pg.evaluate("document.querySelectorAll('#rail .card').length")
    for i in range(min(3, n)):                    # 3 filmi listeye ekle (detay ekrani da cekilir)
        pg.evaluate(f"document.querySelectorAll('#rail .card')[{i}].click()")
        pg.wait_for_selector("#ad", timeout=40000); pg.wait_for_timeout(1200)
        if i == 0: snap(pg, 4)                    # film detayi
        pg.click("#ad"); pg.wait_for_timeout(300); pg.click("#cl"); pg.wait_for_timeout(500)
    pg.click("#n-liste"); pg.wait_for_selector("#liste *", timeout=10000); pg.wait_for_timeout(500)
    snap(pg, 5)                                   # Listem
    b.close()
