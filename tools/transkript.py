# ses.mp3 kelime zamanlari (tek seferlik arac)
import json
from faster_whisper import WhisperModel
m = WhisperModel("small", device="cpu", compute_type="int8")
seg, _ = m.transcribe("ai/reklam/ses.mp3", language="tr", word_timestamps=True)
out = []
for s in seg:
    for w in s.words: out.append({"w": w.word.strip(), "s": round(w.start,2), "e": round(w.end,2)})
json.dump(out, open("ai/reklam/kelimeler.json","w"), ensure_ascii=False, indent=0)
print(" ".join(f"{x['w']}[{x['s']}]" for x in out))
