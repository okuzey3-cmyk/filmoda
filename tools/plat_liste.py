import json, urllib.request
K="91a5fe677d52ce465948f464c3cfd53b"
d=json.load(urllib.request.urlopen(f"https://api.themoviedb.org/3/watch/providers/movie?api_key={K}&watch_region=TR&language=tr-TR"))
r=sorted(d["results"], key=lambda x:(x.get("display_priorities") or {}).get("TR",999))
for p in r[:40]: print(p["provider_id"], p["provider_name"], (p.get("display_priorities") or {}).get("TR"))
# deneme: Netflix filtresiyle discover kac sonuc
for ids in ("8","337","8|337","119"):
    j=json.load(urllib.request.urlopen(f"https://api.themoviedb.org/3/discover/movie?api_key={K}&watch_region=TR&with_watch_providers={ids}&with_watch_monetization_types=flatrate&vote_count.gte=700&vote_average.gte=6.9&without_genres=27,10770&with_genres=35|12"))
    print(ids, j["total_results"], j["total_pages"])
