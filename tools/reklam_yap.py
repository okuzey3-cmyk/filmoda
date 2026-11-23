# Filmoda 30 sn tanitim reklami: gercek uygulama + Turkce erkek sesi + altyazi. Tek seferlik.
import sys, asyncio, base64, functools, http.server, json, os, socketserver, subprocess, threading, time, glob
import edge_tts
from playwright.async_api import async_playwright
OUT = "ai/reklam"; TMP = "/tmp/rk"; os.makedirs(OUT, exist_ok=True); os.makedirs(TMP, exist_ok=True)
VOICE = "tr-TR-AhmetNeural"
SC = [
 "Yemek bitti. Sen seç. Yok, sen seç. Yarım saat geçti, hâlâ film yok.",
 "Tanıdık geldi mi?",
 "Filmoda'da sadece nasıl hissettiğini seç. Dinlenmek mi, gülmek mi, heyecan mı?",
 "Vaktini ve kiminle izleyeceğini söyle.",
 "Sana üç film gelsin. Fragmanı ve nerede izleneceği, hepsi tek ekranda.",
 "Üç film, tek karar.",
 "Filmoda. Ücretsiz, reklamsız, üyeliksiz. Google Play'de.",
]
def sure(f):
    return float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",f]).decode())
async def tts():
    for i, t in enumerate(SC):
        await edge_tts.Communicate(t, VOICE, rate="+10%").save(f"{TMP}/s{i}.mp3")
asyncio.run(tts())
D = [sure(f"{TMP}/s{i}.mp3") + 0.30 for i in range(len(SC))]
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

starts = []; frames = []
async def run():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        c = await b.new_context(viewport={"width":360,"height":640}, device_scale_factor=3, is_mobile=True, has_touch=True, locale="tr-TR")
        pg = await c.new_page()
        await pg.add_init_script("localStorage.setItem('filmoda_intro','1');")
        cdp = await c.new_cdp_session(pg)
        T0 = time.time()
        async def on_frame(e):
            frames.append((time.time()-T0, base64.b64decode(e["data"])))
            try: await cdp.send("Page.screencastFrameAck", {"sessionId": e["sessionId"]})
            except Exception: pass
        cdp.on("Page.screencastFrame", lambda e: asyncio.ensure_future(on_frame(e)))
        await pg.goto("http://127.0.0.1:8198/index.html"); await pg.wait_for_selector("#moods .mood", timeout=30000)
        await cdp.send("Page.startScreencast", {"format":"jpeg","quality":92,"maxWidth":1080,"maxHeight":1920,"everyNthFrame":1})
        await pg.wait_for_timeout(500)
        def basla(i):
            print("sahne", i, flush=True); starts.append(time.time()-T0); return time.time()
        async def bekle(t0, i):
            k = D[i]-(time.time()-t0)
            if k > 0: await pg.wait_for_timeout(int(k*1000))
        async def ev(js): await pg.evaluate(js)
        t = basla(0); await ev("window.scrollTo({top:260,behavior:'smooth'})"); await pg.wait_for_timeout(1500)
        await ev("window.scrollTo({top:0,behavior:'smooth'})"); await bekle(t,0)
        t = basla(1); await bekle(t,1)
        t = basla(2); await pg.wait_for_timeout(700); await ev("document.querySelectorAll('#moods .mood')[1].click()"); await bekle(t,2)
        t = basla(3); await ev("document.querySelectorAll('#sure .chip, #sure button')[1].click()"); await pg.wait_for_timeout(700)
        await ev("document.querySelectorAll('#kim .chip, #kim button')[1].click()"); await pg.wait_for_timeout(300)
        await ev("window.scrollTo({top:document.body.scrollHeight,behavior:'smooth'})"); await pg.wait_for_timeout(900)
        await pg.click("#go"); await bekle(t,3)
        t = basla(4); await pg.wait_for_selector("#rail .card", timeout=40000)
        await pg.wait_for_function("[...document.images].every(i=>i.complete)", timeout=30000); await pg.wait_for_timeout(1300)
        await ev("document.querySelectorAll('#rail .card')[0].click()"); await pg.wait_for_selector("#ad", timeout=40000)
        await bekle(t,4)
        t = basla(5); await ev("document.getElementById('sheet').scrollTo({top:300,behavior:'smooth'})"); await bekle(t,5)
        t = basla(6); await pg.set_content(SON); await bekle(t,6)
        await pg.wait_for_timeout(400); total = time.time()-T0
        await cdp.send("Page.stopScreencast"); await c.close(); await b.close()
        return total
total = asyncio.run(run())
frames[0] = (0.0, frames[0][1])
print("kayit bitti", len(frames), flush=True)
# kareler -> degisken kare hizli video (concat)
os.makedirs(TMP+"/fr", exist_ok=True)
lst = []
for k,(ts,jpg) in enumerate(frames):
    open(f"{TMP}/fr/{k:05d}.jpg","wb").write(jpg)
for k,(ts,jpg) in enumerate(frames):
    nxt = frames[k+1][0] if k+1 < len(frames) else total
    lst.append(f"file '{TMP}/fr/{k:05d}.jpg'\nduration {max(nxt-ts,0.01):.4f}")
lst.append(f"file '{TMP}/fr/{len(frames)-1:05d}.jpg'")
open(TMP+"/frames.txt","w").write("\n".join(lst))
subprocess.check_call(["ffmpeg","-y","-loglevel","error","-f","concat","-safe","0","-i",TMP+"/frames.txt","-vf","fps=30,scale=1080:1920:flags=lanczos,format=yuv420p","-c:v","libx264","-crf","17","-preset","veryfast",TMP+"/ham.mp4"])
vid = TMP+"/ham.mp4"

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
Style: D,DejaVu Sans,50,&H00FFFFFF,&H00000000,&H00000000,1,3,0,2,100,100,110
[Events]
Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text
""" + "\n".join(lines)
open(f"{TMP}/a.ass","w",encoding="utf-8").write(ass)
print('ffmpeg dikey', flush=True)
subprocess.check_call(["ffmpeg","-y","-loglevel","error","-i",vid,"-i",f"{TMP}/ses.m4a","-filter_complex",f"color=c=0x17101A:s=1080x1920:d=120[bg];[0:v]scale=900:1600:flags=lanczos[p];[bg][p]overlay=90:40:shortest=1,ass={TMP}/a.ass,format=yuv420p[v]","-map","[v]","-map","1:a",
  "-c:v","libx264","-crf","20","-preset","veryfast","-r","30","-c:a","aac","-b:a","160k","-shortest","-movflags","+faststart",f"{OUT}/filmoda-reklam-dikey.mp4"])
print('yatay', flush=True)
# yatay 16:9: telefon ortada, koyu zemin
subprocess.check_call(["ffmpeg","-y","-loglevel","error","-i",f"{OUT}/filmoda-reklam-dikey.mp4","-filter_complex",
  "color=c=0x17101A:s=1920x1080:d=60[bg];[0:v]scale=-2:1080[v];[bg][v]overlay=(W-w)/2:0:shortest=1,format=yuv420p","-c:v","libx264","-crf","20","-preset","veryfast","-c:a","copy","-movflags","+faststart",f"{OUT}/filmoda-reklam-yatay.mp4"])
for k, s in enumerate([3, 12, 19, 27]):
    subprocess.call(["ffmpeg","-y","-loglevel","error","-ss",str(s),"-i",f"{OUT}/filmoda-reklam-dikey.mp4","-frames:v","1","-vf","scale=360:-2",f"{OUT}/kare{k}.png"])
print("tamam", total, starts)
