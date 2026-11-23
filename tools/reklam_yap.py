# Filmoda 30 sn tanitim reklami: gercek uygulama + Turkce erkek sesi + altyazi. Tek seferlik.
import sys, asyncio, base64, functools, http.server, json, os, socketserver, subprocess, threading, time, glob

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
SES="ai/reklam/ses.mp3"
ZAMAN=json.load(open("ai/reklam/zaman.json"))   # sahne baslangiclari (sn) + kuyruk
SB=ZAMAN["sahne"]; SES_SURE=sure(SES); KUYRUK=ZAMAN.get("kuyruk",1.0)
D=[(SB[i+1] if i+1<len(SB) else SES_SURE+KUYRUK)-SB[i] for i in range(len(SC))]
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

starts = []; frames = []; CUT = []
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
        t = basla(2); await pg.wait_for_timeout(500); await ev("document.querySelectorAll('#moods .mood')[1].click()"); await bekle(t,2)
        t = basla(3); await ev("document.querySelectorAll('#sure .chip, #sure button')[1].click()"); await pg.wait_for_timeout(450)
        await ev("document.querySelectorAll('#kim .chip, #kim button')[1].click()"); await pg.wait_for_timeout(150)
        await ev("window.scrollTo({top:document.body.scrollHeight,behavior:'smooth'})"); await pg.wait_for_timeout(600)
        await bekle(t,3)
        ca = time.time()-T0; await pg.click("#go")
        t = basla(4); await pg.wait_for_selector("#rail .card", timeout=40000)
        await pg.wait_for_function("(()=>{const a=[...document.querySelectorAll('#rail .card img')];return a.length>=2&&a.every(i=>i.complete&&i.naturalWidth>0)})()", timeout=40000); await pg.wait_for_timeout(900)
        cb = time.time()-T0; CUT.append((ca+0.15, cb)); t = time.time(); await pg.wait_for_timeout(2200)
        await ev("document.querySelectorAll('#rail .card')[0].click()"); await pg.wait_for_selector("#ad", timeout=40000)
        await bekle(t,4)
        t = basla(5); await ev("document.getElementById('sheet').scrollTo({top:300,behavior:'smooth'})"); await bekle(t,5)
        t = basla(6); await pg.set_content(SON); await bekle(t,6)
        await pg.wait_for_timeout(400); total = time.time()-T0
        await cdp.send("Page.stopScreencast"); await c.close(); await b.close()
        return total
total = asyncio.run(run())
if CUT:
    ca, cb = CUT[0]; L = cb-ca
    frames[:] = [(ts if ts<=ca else ts-L, j) for ts,j in frames if not (ca<ts<cb)]
    for i in range(5, len(starts)): starts[i] -= L
    total -= L
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

subprocess.check_call(["ffmpeg","-y","-loglevel","error","-i",SES,"-af",f"adelay={int(starts[0]*1000)}|{int(starts[0]*1000)},apad=whole_dur={total:.3f}","-ar","44100","-ac","2",f"{TMP}/ses.m4a"])
# ---- muzik + efekt (ozgun, sentezlenmis) ----
import numpy as np, wave
SR=44100
def nota(m): return 440.0*2**((m-69)/12)
def yaz(path, x):
    x=np.clip(x,-1,1); d=(x*32767).astype(np.int16)
    w=wave.open(path,"wb"); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(d.tobytes()); w.close()
def muzik_uret(toplam, sfx_t):
    n=int(SR*(toplam+1.5)); L=np.zeros(n); R=np.zeros(n)
    bpm=100.0; beat=60.0/bpm; t=np.arange(n)/SR
    akor=[(57,60,64),(53,57,60),(48,52,55),(55,59,62)]   # Am F C G
    bar=4*beat
    for k in range(int((toplam+1.5)/bar)+2):
        ch=akor[k%4]; a=int(k*bar*SR); b=min(n,int((k+1)*bar*SR+0.6*SR))
        if a>=n: break
        tt=np.arange(b-a)/SR; env=np.minimum(tt/0.6,1)*np.minimum((b-a)/SR-tt,0.9)/0.9; env=np.clip(env,0,1)
        for m in ch:
            f=nota(m)
            v=(np.sin(2*np.pi*f*tt)+0.4*np.sin(2*np.pi*f*1.004*tt)+0.25*np.sin(2*np.pi*2*f*tt))*env*0.07
            L[a:b]+=v; R[a:b]+=v*0.9
        # bas
        fb=nota(ch[0]-12); vb=np.sin(2*np.pi*fb*tt)*env*0.16; L[a:b]+=vb; R[a:b]+=vb
    # arpej (8'lik)
    e8=beat/2
    for i in range(int((toplam+1.5)/e8)):
        tm=i*e8
        if tm<2.0: continue
        ch=akor[int(tm//bar)%4]; m=[ch[0]+12,ch[1]+12,ch[2]+12,ch[1]+24][i%4]
        a=int(tm*SR); L2=int(0.5*SR); b=min(n,a+L2)
        if a>=n: break
        tt=np.arange(b-a)/SR; v=np.sin(2*np.pi*nota(m)*tt)*np.exp(-tt*7)*0.07
        pan=0.3+0.4*((i%4)/3.0); L[a:b]+=v*(1-pan); R[a:b]+=v*pan
    # davul: 7. saniyeden sonra
    for i in range(int((toplam+1.5)/beat)):
        tm=i*beat
        if tm<7.0: continue
        a=int(tm*SR)
        if a>=n: break
        if i%2==0:
            tt=np.arange(min(int(0.3*SR),n-a))/SR; f=110*np.exp(-tt*18)+45
            v=np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-tt*9)*0.5; L[a:a+len(tt)]+=v; R[a:a+len(tt)]+=v
        h=a+int(beat*SR/2)
        if h<n:
            tt=np.arange(min(int(0.06*SR),n-h))/SR; v=(np.random.randn(len(tt)))*np.exp(-tt*70)*0.05
            L[h:h+len(tt)]+=v; R[h:h+len(tt)]+=v
    # gecis efekti (whoosh)
    rng=np.random.RandomState(7)
    for st in sfx_t:
        a=int(max(0,st-0.35)*SR); ln=int(0.5*SR)
        if a+ln>=n: continue
        tt=np.arange(ln)/SR; ns=rng.randn(ln); k=np.convolve(ns,np.ones(40)/40,mode="same")
        env=np.sin(np.pi*tt/0.5)**2; v=k*env*0.35
        L[a:a+ln]+=v; R[a:a+ln]+=v
    ft=int(1.5*SR); fade=np.ones(n); fade[-ft:]=np.linspace(1,0,ft); fade[:int(0.5*SR)]=np.linspace(0,1,int(0.5*SR))
    return np.stack([L*fade,R*fade],axis=1).reshape(-1)*0.9
yaz(TMP+"/muzik.wav", muzik_uret(total, [starts[2],starts[4],starts[6]]))
subprocess.check_call(["ffmpeg","-y","-loglevel","error","-i",TMP+"/ses.m4a","-i",TMP+"/muzik.wav","-filter_complex",
  "[1:a]volume=0.9[m];[0:a]asplit=2[v1][v2];[m][v1]sidechaincompress=threshold=0.02:ratio=9:attack=15:release=350:makeup=1[duck];[duck][v2]amix=inputs=2:normalize=0,loudnorm=I=-16:TP=-1.5[aout]",
  "-map","[aout]","-ar","44100",TMP+"/ses2.m4a"])
# altyazi (ASS)
def ass_t(s): h=int(s//3600); m=int(s%3600//60); return f"{h}:{m:02d}:{s%60:05.2f}"
lines = []
for i, t in enumerate(SC):
    b0 = SB[i]+starts[0]; e = (SB[i+1]+starts[0]-0.05) if i<len(SC)-1 else b0+D[i]-0.4
    lines.append(f"Dialogue: 0,{ass_t(b0+0.02)},{ass_t(e)},D,,0,0,0,,{t}")
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
subprocess.check_call(["ffmpeg","-y","-loglevel","error","-i",vid,"-i",f"{TMP}/ses2.m4a","-filter_complex",f"color=c=0x17101A:s=1080x1920:d=120[bg];[0:v]scale=w='900*(1+0.05*t/{total:.1f})':h='1600*(1+0.05*t/{total:.1f})':eval=frame:flags=bilinear[p];[bg][p]overlay=x='(W-w)/2':y='40':shortest=1,ass={TMP}/a.ass,format=yuv420p[v]","-map","[v]","-map","1:a",
  "-c:v","libx264","-crf","20","-preset","veryfast","-r","30","-c:a","aac","-b:a","160k","-shortest","-movflags","+faststart",f"{OUT}/filmoda-reklam-dikey.mp4"])
print('yatay', flush=True)
# yatay 16:9: telefon ortada, koyu zemin
subprocess.check_call(["ffmpeg","-y","-loglevel","error","-i",f"{OUT}/filmoda-reklam-dikey.mp4","-filter_complex",
  "color=c=0x17101A:s=1920x1080:d=60[bg];[0:v]scale=-2:1080[v];[bg][v]overlay=(W-w)/2:0:shortest=1,format=yuv420p","-c:v","libx264","-crf","20","-preset","veryfast","-c:a","copy","-movflags","+faststart",f"{OUT}/filmoda-reklam-yatay.mp4"])
for k, s in enumerate([3, 12, 19, 27]):
    subprocess.call(["ffmpeg","-y","-loglevel","error","-ss",str(s),"-i",f"{OUT}/filmoda-reklam-dikey.mp4","-frames:v","1","-vf","scale=360:-2",f"{OUT}/kare{k}.png"])
print("tamam", total, starts)
