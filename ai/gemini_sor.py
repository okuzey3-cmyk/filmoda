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

def pick_model():
    req = urllib.request.Request(f"{BASE}/models?pageSize=200", headers={"x-goog-api-key": KEY})
    with urllib.request.urlopen(req, timeout=60) as r:
        ms = json.load(r).get("models", [])
    ok = [m["name"].split("/")[1] for m in ms
          if "generateContent" in m.get("supportedGenerationMethods", [])
          and "flash" in m["name"] and "lite" not in m["name"]
          and not any(x in m["name"] for x in ("image", "tts", "live", "audio", "thinking", "preview", "exp"))]
    ok.sort(reverse=True)
    return ok[0] if ok else None

soru = open("ai/soru.md", encoding="utf-8").read()
sistem = open("ai/baglam.md", encoding="utf-8").read()
kod = open("index.html", encoding="utf-8").read()[:150000]
gecmis = ""
for f in sorted(glob.glob("ai/tur-*.md"))[-4:]:
    gecmis += f"\n\n--- {f} ---\n" + open(f, encoding="utf-8").read()[:6000]

tam = (sistem + "\n\n=== UYGULAMANIN KODU (index.html) ===\n" + kod +
       "\n\n=== ONCEKI TURLAR ===" + gecmis + "\n\n=== CLAUDE'UN SORUSU ===\n" + soru)

try:
    cevap = call(MODEL, tam)
    kullanilan = MODEL
except urllib.error.HTTPError as e:
    if e.code in (400, 404):
        m = pick_model()
        if not m:
            raise
        cevap = call(m, tam)
        kullanilan = m
    else:
        print("HTTP", e.code, e.read().decode()[:500])
        raise

n = len(glob.glob("ai/tur-*.md")) + 1
with open(f"ai/tur-{n:02d}-gemini.md", "w", encoding="utf-8") as f:
    f.write(f"# Tur {n} - Gemini cevabi (model: {kullanilan})\n\n{cevap}\n")
print("ok", kullanilan, n)
