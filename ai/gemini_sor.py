import os, sys, json, glob, urllib.request, urllib.error

KEY = os.environ["GEMINI_API_KEY"]
MODEL = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")
BASE = "https://generativelanguage.googleapis.com/v1beta"

def call(model, text):
    body = {"contents": [{"role": "user", "parts": [{"text": text}]}],
            "generationConfig": {"temperature": 0.7, "maxOutputTokens": 8192}}
    req = urllib.request.Request(
        f"{BASE}/models/{model}:generateContent",
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json", "x-goog-api-key": KEY})
    with urllib.request.urlopen(req, timeout=180) as r:
        d = json.load(r)
    return "".join(p.get("text", "") for p in d["candidates"][0]["content"]["parts"])

def liste_modeller():
    req = urllib.request.Request(f"{BASE}/models?pageSize=200", headers={"x-goog-api-key": KEY})
    with urllib.request.urlopen(req, timeout=60) as r:
        ms = json.load(r).get("models", [])
    ad = [m["name"].split("/")[1] for m in ms if "generateContent" in m.get("supportedGenerationMethods", [])]
    open("ai/modeller.txt", "w").write("\n".join(ad))
    iyi = [x for x in ad if ("flash" in x or "pro" in x or "gemma" in x)
           and not any(t in x for t in ("image", "tts", "live", "audio", "omni", "embedding", "robotics", "computer", "vision"))]
    # once flash (lite hari), sonra lite, sonra pro, sonra gemma
    def sira(x):
        return (0 if ("flash" in x and "lite" not in x) else 1 if "lite" in x else 2 if "pro" in x else 3, x)
    return sorted(iyi, key=sira)

import traceback
def main():
    soru = open("ai/soru.md", encoding="utf-8").read()
    sistem = open("ai/baglam.md", encoding="utf-8").read()
    if os.path.exists("ai/arastirma.md"):
        sistem += "\n\n=== PIYASA ARASTIRMASI (Claude topladi) ===\n" + open("ai/arastirma.md", encoding="utf-8").read()
    kod = open("index.html", encoding="utf-8").read()[:150000]
    gecmis = ""
    for f in sorted(glob.glob("ai/tur-*.md"))[-5:]:
        gecmis += f"\n\n--- {f} ---\n" + open(f, encoding="utf-8").read()[:6000]

    tam = (sistem + "\n\n=== UYGULAMANIN KODU (index.html) ===\n" + kod +
           "\n\n=== ONCEKI TURLAR ===" + gecmis + "\n\n=== CLAUDE'UN SORUSU ===\n" + soru)

    adaylar = [MODEL] + [m for m in liste_modeller() if m != MODEL]
    kullanilan = None
    sonhata = ""
    deneme = []
    for m in adaylar[:14]:
        try:
            cevap = call(m, tam)
            kullanilan = m
            break
        except urllib.error.HTTPError as e:
            deneme.append(f"{m}: HTTP {e.code}")
            sonhata = e.read().decode()[:300]
            if e.code not in (400, 404, 429, 503):
                raise
    if not kullanilan:
        open("ai/hata.md", "w", encoding="utf-8").write("Hicbir model calismadi\n" + "\n".join(deneme) + "\n" + sonhata.replace(KEY, "***"))
        return
    if os.path.exists("ai/hata.md"):
        os.remove("ai/hata.md")
    n = len(glob.glob("ai/tur-*-gemini.md")) + 1
    with open(f"ai/tur-{n:02d}-gemini.md", "w", encoding="utf-8") as f:
        f.write(f"# Tur {n} - Gemini cevabi (model: {kullanilan})\n\n{cevap}\n")
    print("ok", kullanilan, n)

try:
    main()
except urllib.error.HTTPError as e:
    msg=e.read().decode()[:1500]
    open('ai/hata.md','w',encoding='utf-8').write('HTTP %s\n%s\n'%(e.code,msg.replace(KEY,'***')))
    print('HTTP',e.code)
except Exception:
    open('ai/hata.md','w',encoding='utf-8').write(traceback.format_exc().replace(KEY,'***'))
    print('HATA')
