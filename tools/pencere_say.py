# Sayfa penceresi genisletmenin etkisi: erisilebilir film sayisi ve kalite (once/sonra). Tek seferlik olcum.
import json, re, time, urllib.request, urllib.parse
from concurrent.futures import ThreadPoolExecutor
html = open("index.html", encoding="utf-8").read()
KEY = re.search(r'KEY *= *"([a-f0-9]{32})"', html).group(1)
MOODS = {"sakin":"16|10751|10749|14","neseli":"35|12","duygusal":"18|10749","heyecan":"28|53|9648","dusunce":"878|9648|53"}
V = {"tek":700,"iki":1500,"arkadas":2500,"aile":800}
def get(p):
    p = dict(p); p["api_key"] = KEY; p["language"] = "tr-TR"
    url = "https://api.themoviedb.org/3/discover/movie?" + urllib.parse.urlencode(p)
    for i in range(4):
        try:
            with urllib.request.urlopen(url, timeout=30) as r: return json.load(r)
        except Exception: time.sleep(1.5*(i+1))
    return {}
cache = {}
def sayfa(q, n):
    k = (json.dumps(q, sort_keys=True), n)
    if k not in cache:
        r = get(dict(q, page=n)); cache[k] = [(x["id"], x.get("vote_average",0), x.get("vote_count",0), x.get("release_date","")[:4]) for x in r.get("results", [])]
    return cache[k]
def erisim(q, win):
    out = []
    with ThreadPoolExecutor(8) as ex:
        for lst in ex.map(lambda n: sayfa(q, n), range(1, win+1)): out += lst
    return out
SENARYO = {"simdi": (6,3,3,2), "genis": (15,8,8,3)}
sonuc = {s: {} for s in SENARYO}; tum = {s: {} for s in SENARYO}
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
        for s, wins in SENARYO.items():
            u = {}
            for q, w in zip(qs, wins):
                for (i, a, c, y) in erisim(q, w): u[i] = (a, c, y)
            sonuc[s][kim+"/"+mood] = u
        print(kim, mood, len(sonuc["simdi"][kim+"/"+mood]), len(sonuc["genis"][kim+"/"+mood]), flush=True)
def ozet(s):
    allids = {}
    for k, u in sonuc[s].items(): allids.update(u)
    vals = list(allids.values())
    n = len(vals)
    ort = sum(a for a,_,_ in vals)/n
    dusuk = sum(1 for a,_,_ in vals if a < 7.0)
    eski = sum(1 for _,_,y in vals if y and int(y) < 1980)
    medv = sorted(c for _,c,_ in vals)[n//2]
    return n, ort, dusuk, eski, medv
with open("ai/pencere.md", "w", encoding="utf-8") as f:
    f.write("# Sayfa penceresi olcumu (%s)\n\n" % time.strftime("%Y-%m-%d"))
    f.write("Pencereler (pop, puan1, puan2, tr): simdi=%s, genis=%s\n\n" % (SENARYO["simdi"], SENARYO["genis"]))
    f.write("| Kim | Mood | simdi | genis |\n|---|---|---|---|\n")
    for kim in V:
        for mood in MOODS:
            k = kim+"/"+mood
            f.write("| %s | %s | %d | %d |\n" % (kim, mood, len(sonuc["simdi"][k]), len(sonuc["genis"][k])))
    f.write("\n## Toplam (tum kombinasyonlar, benzersiz)\n\n| Senaryo | Film | Ort. puan | Puani <7.0 olan | 1980 oncesi | Medyan oy sayisi |\n|---|---|---|---|---|---|\n")
    for s in SENARYO:
        n, ort, d, e, m = ozet(s)
        f.write("| %s | %d | %.2f | %d | %d | %d |\n" % (s, n, ort, d, e, m))
print("bitti")
