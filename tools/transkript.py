# ses.mp3 kelime zamanlari (tek seferlik arac)
import json, subprocess
import numpy as np
from faster_whisper import WhisperModel
m = WhisperModel("small", device="cpu", compute_type="int8")
raw = subprocess.check_output(["ffmpeg","-v","error","-i","ai/reklam/ses.mp3","-f","f32le","-ac","1","-ar","16000","-"])
au = np.frombuffer(raw, dtype=np.float32)
seg, _ = m.transcribe(au, language="tr", word_timestamps=True)
out = []
for s in seg:
    for w in s.words: out.append({"w": w.word.strip(), "s": round(w.start,2), "e": round(w.end,2)})
json.dump(out, open("ai/reklam/kelimeler.json","w"), ensure_ascii=False, indent=0)
print(" ".join(f"{x['w']}[{x['s']}]" for x in out))
