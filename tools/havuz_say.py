# Filmoda havuz boyutu olcumu (tek seferlik). index.html havuz() sartlarini taklit eder.
import json, os, re, sys, time, urllib.request, urllib.parse
from concurrent.futures import ThreadPoolExecutor
html = open("index.html", encoding="utf-8").read()
KEY = re.search(r'KEY *= *"([a-f0-9]{32})"', html).group(1)
MOODS = {"sakin":"16|10751|10749|14","neseli":"35|12","duygusal":"18|10749","heyecan":"28|53|9648","dusunce":"878|9648|53"}
V = {"tek":700,"iki":1500,"arkadas":2500,"aile":800}
def get(path, p):
    p = dict(p); p["api_key"] = KEY; p["language"] = "tr-TR"
    url = "https://api.themoviedb.org/3" + path + "?" + urllib.parse.urlencode(p)
    for i in range(4):
        try:
            with urllib.request.urlopen(url, timeout=30) as r: return json.load(r)
        except Exception as e:
            time.sleep(1.5*(i+1))
    return {}
def tum_idler(extra):
    ids = set(); d = get("/discover/movie", dict(extra, page=1)); tp = min(d.get("total_pages", 0), 500)
    for x in d.get("results", []): ids.add(x["id"])
    def pg(n):
        r = get("/discover/movie", dict(extra, page=n)); return [x["id"] for x in r.get("results", [])]
    with ThreadPoolExecutor(8) as ex:
        for lst in ex.map(pg, range(2, tp+1)):
            ids.update(lst)
    return ids, d.get("total_results", 0)
sonuc = {}; hepsi = set()
for kim in V:
    for mood, g in MOODS.items():
        gen = g
        if kim == "aile": gen = "10751|16"
        elif kim == "arkadas": gen = g + "|35|28|12"
        yasak = "27,10770,80,10752" if kim == "aile" else "27,10770"
        base = {"include_adult":"false","without_genres":yasak,"with_genres":gen}
        v = V[kim]
        qs = [
          dict(base, sort_by="popularity.desc", **{"vote_count.gte":str(v),"vote_average.gte":"6.9"}),
          dict(base, sort_by="vote_average.desc", **{"vote_count.gte":str(max(v,3000)),"vote_average.gte":"7.4"}),
          dict(base, sort_by="vote_average.desc", **{"vote_count.gte":"800","vote_count.lte":"5000","vote_average.gte":"7.3"}),
          dict(base, with_original_language="tr", sort_by="popularity.desc", **{"vote_count.gte":"200","vote_average.gte":"7"}),
        ]
        u = set()
        for q in qs:
            ids, _ = tum_idler(q); u |= ids
        sonuc[kim+"/"+mood] = len(u); hepsi |= u
        print(kim, mood, len(u), flush=True)
os.makedirs("ai", exist_ok=True)
with open("ai/havuz.md", "w", encoding="utf-8") as f:
    f.write("# Filmoda havuz olcumu (%s)\n\n" % time.strftime("%Y-%m-%d"))
    f.write("Toplam benzersiz film (tum ruh hali ve kim kombinasyonlari, sure: fark etmez): **%d**\n\n" % len(hepsi))
    f.write("| Kim | " + " | ".join(MOODS) + " |\n|---|" + "---|"*len(MOODS) + "\n")
    for kim in V:
        f.write("| %s | " % kim + " | ".join(str(sonuc[kim+"/"+m]) for m in MOODS) + " |\n")
    f.write("\nNot: Her sorgunun tum sayfalari taranmistir (TMDB en fazla 500 sayfa/10.000 sonuc verir). Seviye-2 kisisel adaylar dahil degildir.\n")
print("TOPLAM", len(hepsi))
