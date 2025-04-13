import requests
import json

API_KEY = "8bb57fb34476880013cbe2f37d283451"
headers = {
    "x-apisports-key": API_KEY
}

# Získání všech zápasů pro dnešní den
print("Zkouším dotaz na API...")
url = "https://v3.football.api-sports.io/fixtures?season=2023&next=500"
response = requests.get(url, headers=headers)
print("STATUS:", response.status_code)
print("ODPOVĚĎ:", response.text[:500])  # vypíše prvních 500 znaků odpovědi
exit()  # dočasně ukončí skript tady

# Výpočet výsledků 0:0 podle ligy a kola
results = {}
for match in fixtures:
    league = match["league"]["name"]
    round_ = match["league"]["round"]
    goals = match["goals"]
    status = match["fixture"]["status"]["short"]

    key = (league, round_)
    if key not in results:
        results[key] = {"draws_0_0": 0, "matches": 0, "remaining": 0}

    if status == "FT":
        results[key]["matches"] += 1
        if goals["home"] == 0 and goals["away"] == 0:
            results[key]["draws_0_0"] += 1
    elif status in ("NS", "TBD"):
        results[key]["remaining"] += 1

# Převod na výstupní strukturu
output = []
for (league, round_), data in results.items():
    output.append({
        "league": league,
        "round": round_,
        "draws_0_0": data["draws_0_0"],
        "max_draws": 3,
        "remaining": data["remaining"]
    })

# Uložení jako data.json
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(output, f, indent=2, ensure_ascii=False)
