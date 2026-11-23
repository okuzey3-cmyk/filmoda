import json, urllib.request
K="91a5fe677d52ce465948f464c3cfd53b"
d=json.load(urllib.request.urlopen(f"https://api.themoviedb.org/3/watch/providers/movie?api_key={K}&watch_region=TR&language=tr-TR"))
for p in d["results"]:
    n=p["provider_name"].lower()
    if any(k in n for k in ("apple","blu","gain","tabii","exxen","hbo","tv+","mubi","puhu","disney","prime")): print("LISTE", p["provider_id"], p["provider_name"], (p.get("display_priorities") or {}).get("TR"))
for ids in ("350","1899","1904","1791","11","342","8|119|337","1899|1904|1791|11|342|350"):
    j=json.load(urllib.request.urlopen(f"https://api.themoviedb.org/3/discover/movie?api_key={K}&watch_region=TR&with_watch_providers={ids}&with_watch_monetization_types=flatrate&vote_count.gte=300&vote_average.gte=6.6&without_genres=27,10770"))
    print("SAYI", ids, j["total_results"])
