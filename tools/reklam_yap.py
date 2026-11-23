# Filmoda 30 sn tanitim reklami: gercek uygulama + Turkce erkek sesi + altyazi. Tek seferlik.
import sys, asyncio, base64, functools, http.server, json, os, socketserver, subprocess, threading, time, glob
import edge_tts
from playwright.sync_api import sync_playwright
OUT = "ai/reklam"; TMP = "/tmp/rk"; os.makedirs(OUT, exist_ok=True); os.makedirs(TMP, exist_ok=True)
VOICE = "tr-TR-AhmetNeural"
SC = [
 "Yemek bitti, kanepeye oturdun. Sen seç. Yok, sen seç. Yarım saat geçti, hâlâ film yok.",
 "Tanıdık geldi mi?",
 "Filmoda'da sadece nasıl hissettiğini seç. Dinlenmek mi istiyorsun, gülmek mi, heyecan mı?",
 "Ne kadar vaktin var, kiminle izleyeceksin, onu da söyle.",
 "Sana tam üç film gelsin. Fragmanı, nerede izleneceği, hepsi tek ekranda.",
 "Üç film, tek karar.",
 "Filmoda. Ücretsiz, reklamsız, üyeliksiz. Google Play'de.",
]
def sure(f):
    return float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",f]).decode())
async def tts():
    for i, t in enumerate(SC):
        await edge_tts.Communicate(t, VOICE, rate="-4%").save(f"{TMP}/s{i}.mp3")
asyncio.run(tts())
D = [sure(f"{TMP}/s{i}.mp3") + 0.45 for i in range(len(SC))]
print("sureler", D, flush=True)
class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
srv = socketserver.TCPServer(("127.0.0.1", 8198), functools.partial(Q, directory="."))
threading.Thread(target=srv.serve_forever, daemon=True).start()
ikon = base64.b64encode(open("icon-512.png","rb").read()).decode()
SON = f"""<body style="margin:0;background:#17101A;color:#fff;font-family:Georgia,serif;display:flex;flex-direction:column;align-items:center;justify-content:center;height:100vh;text-align:center">
<img src="data:image/png;base64,{ikon}" style="width:120px;height:120px;border-radius:28px">
<div style="font-size:44px;margin-top:22px;font-weight:700">Filmoda</div>
<div style="font-size:16px;color:#E8899D;margin-top:8px;font-family:Arial,sans-serif">Bu akşam ne izlesem?</div>
<div style="margin-top:34px;padding:12px 22px;border:1px solid #5a4a62;border-radius:14px;font-family:Arial,sans-serif;font-size:15px">Google Play'de ücretsiz</div></body>"""
starts = []
with sync_playwright() as p:
    b = p.chromium.launch()
    c = b.new_context(viewport={"width":360,"height":640}, device_scale_factor=3, is_mobile=True, has_touch=True, locale="tr-TR",
                      record_video_dir=TMP+"/vid", record_video_size={"width":1080,"height":1920})
    pg = c.new_page(); T0 = time.time()
    pg.add_init_script("localStorage.setItem('filmoda_intro','1');")
    def basla(i):
        starts.append(time.time()-T0); return time.time()
    def bekle(t0, i):
        k = D[i]-(time.time()-t0)
        if k > 0: pg.wait_for_timeout(int(k*1000))
    pg.goto("http://127.0.0.1:8198/index.html"); pg.wait_for_selector("#moods .mood", timeout=30000); pg.wait_for_timeout(500)
    # 0
    print('sahne0', flush=True); t = basla(0); pg.evaluate("window.scrollTo({top:260,behavior:'smooth'})"); pg.wait_for_timeout(1800)
    pg.evaluate("window.scrollTo({top:0,behavior:'smooth'})"); bekle(t,0)
    # 1
    print('sahne1', flush=True); t = basla(1); bekle(t,1)
    # 2
    print('sahne2', flush=True); t = basla(2); pg.wait_for_timeout(900); pg.evaluate("document.querySelectorAll('#moods .mood')[1].click()"); bekle(t,2)
    # 3
    print('sahne3', flush=True); t = basla(3); pg.evaluate("document.querySelectorAll('#sure .chip, #sure button')[1].click()"); pg.wait_for_timeout(1100)
    pg.evaluate("document.querySelectorAll('#kim .chip, #kim button')[1].click()"); pg.wait_for_timeout(500)
    pg.evaluate("window.scrollTo({top:document.body.scrollHeight,behavior:'smooth'})"); bekle(t,3)
    # 4
    print('sahne4', flush=True); t = basla(4); pg.click("#go"); pg.wait_for_selector("#rail .card", timeout=40000)
    pg.wait_for_function("[...document.images].every(i=>i.complete)", timeout=30000); pg.wait_for_timeout(1800)
    pg.evaluate("document.querySelectorAll('#rail .card')[0].click()"); pg.wait_for_selector("#ad", timeout=40000)
    bekle(t,4)
    # 5
    print('sahne5', flush=True); t = basla(5); pg.evaluate("document.getElementById('sheet').scrollTo({top:300,behavior:'smooth'})"); bekle(t,5)
    # 6
    print('sahne6', flush=True); t = basla(6); pg.set_content(SON); bekle(t,6)
    total = time.time()-T0; pg.wait_for_timeout(300)
    c.close(); b.close()
print('kayit bitti', flush=True)
vid = glob.glob(TMP+"/vid/*.webm")[0]
# ses: her sahne kendi baslangicinda
inputs = []; flt = []
for i in range(len(SC)):
    inputs += ["-i", f"{TMP}/s{i}.mp3"]
    flt.append(f"[{i}:a]adelay={int(starts[i]*1000)}|{int(starts[i]*1000)}[a{i}]")
mix = "".join(f"[a{i}]" for i in range(len(SC))) + f"amix=inputs={len(SC)}:normalize=0[aout]"
subprocess.check_call(["ffmpeg","-y","-loglevel","error"]+inputs+["-filter_complex",";".join(flt)+";"+mix,"-map","[aout]",f"{TMP}/ses.m4a"])
# altyazi (ASS)
def ass_t(s): h=int(s//3600); m=int(s%3600//60); return f"{h}:{m:02d}:{s%60:05.2f}"
lines = []
for i, t in enumerate(SC):
    e = starts[i]+D[i]-0.1
    lines.append(f"Dialogue: 0,{ass_t(starts[i]+0.05)},{ass_t(e)},D,,0,0,0,,{t}")
ass = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 0
[V4+ Styles]
Format: Name,Fontname,Fontsize,PrimaryColour,OutlineColour,BackColour,Bold,Outline,Shadow,Alignment,MarginL,MarginR,MarginV
Style: D,DejaVu Sans,54,&H00FFFFFF,&HCC000000,&H00000000,1,5,0,2,90,90,330
[Events]
Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text
""" + "\n".join(lines)
open(f"{TMP}/a.ass","w",encoding="utf-8").write(ass)
print('ffmpeg dikey', flush=True)
subprocess.check_call(["ffmpeg","-y","-loglevel","error","-i",vid,"-i",f"{TMP}/ses.m4a","-vf",f"scale=1080:1920:flags=lanczos,ass={TMP}/a.ass,format=yuv420p",
  "-c:v","libx264","-crf","20","-preset","veryfast","-r","30","-c:a","aac","-b:a","160k","-shortest","-movflags","+faststart",f"{OUT}/filmoda-reklam-dikey.mp4"])
print('yatay', flush=True)
# yatay 16:9: telefon ortada, koyu zemin
subprocess.check_call(["ffmpeg","-y","-loglevel","error","-i",f"{OUT}/filmoda-reklam-dikey.mp4","-filter_complex",
  "color=c=0x17101A:s=1920x1080[bg];[0:v]scale=-2:1080[v];[bg][v]overlay=(W-w)/2:0,format=yuv420p","-c:v","libx264","-crf","20","-preset","veryfast","-c:a","copy","-movflags","+faststart",f"{OUT}/filmoda-reklam-yatay.mp4"])
for k, s in enumerate([3, 12, 19, 27]):
    subprocess.call(["ffmpeg","-y","-loglevel","error","-ss",str(s),"-i",f"{OUT}/filmoda-reklam-dikey.mp4","-frames:v","1","-vf","scale=360:-2",f"{OUT}/kare{k}.png"])
print("tamam", total, starts)
