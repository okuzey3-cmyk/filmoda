import json, re, time, urllib.request, urllib.parse
html = open("index.html", encoding="utf-8").read()
KEY = re.search(r'KEY *= *"([a-f0-9]{32})"', html).group(1)
def say(**p):
    p.update(api_key=KEY, include_adult="false", page=1)
    url = "https://api.themoviedb.org/3/discover/movie?" + urllib.parse.urlencode(p)
    for i in range(4):
        try:
            with urllib.request.urlopen(url, timeout=30) as r: return json.load(r)["total_results"]
        except Exception: time.sleep(2*(i+1))
    return -1
rows = []
for puan in ("6.5", "7.0", "7.5"):
    for oy in (200, 500, 1000, 3000):
        rows.append((puan, oy, say(**{"vote_average.gte": puan, "vote_count.gte": str(oy)})))
tr = say(**{"vote_average.gte": "7.0", "vote_count.gte": "200", "with_original_language": "tr"})
tum = say(**{"vote_count.gte": "1"})
with open("ai/iyi.md", "w", encoding="utf-8") as f:
    f.write("# Iyi film sayisi (TMDB, yetiskin icerik haric, %s)\n\n" % time.strftime("%Y-%m-%d"))
    f.write("Oy verilmis (en az 1 oy) toplam film: %d\n\n| Min puan | Min oy | Film sayisi |\n|---|---|---|\n" % tum)
    for p, o, n in rows: f.write("| %s | %d | %d |\n" % (p, o, n))
    f.write("\nTurkce film (puan>=7.0, oy>=200): %d\n" % tr)
print(open("ai/iyi.md", encoding="utf-8").read())
