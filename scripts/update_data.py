import requests
import json
from datetime import date

API_KEY = "8bb57fb34476880013cbe2f37d283451"
headers = {
    "x-apisports-key": API_KEY
}

# Získání všech zápasů pro dnešní den
today = date.today().isoformat()
url = f"https://v3.football.api-sports.io/fixtures?date=2025-04-13"
response = requests.get(url, headers=headers)
fixtures = response.json().get("response", [])

# Výpočet výsledků 0:0 podle ligy a kola
results = {}

for match in fixtures:
    league_raw = match.get("league")

    if isinstance(league_raw, dict):
        country_raw = league_raw.get("country")
        if isinstance(country_raw, dict):
            country = country_raw.get("name", "Neznámý stát")
        else:    
            country = "Neznámý stát"

        league_name = f'{country} – {league_raw.get("name", "Neznámá liga")}'
    else:
        country = "Neznámý stát"
        league_name = f'{country} – {league_raw}'
        round_ = match["league"]["round"]
        goals = match["goals"]
        status = match["fixture"]["status"]["short"]

    if status != "FT":
        continue

    key = (league, round_)
    if key not in results:
        results[key] = {"draws_0_0": 0, "matches": 0}

    results[key]["matches"] += 1
    if goals["home"] == 0 and goals["away"] == 0:
        results[key]["draws_0_0"] += 1

# Převod na výstupní strukturu
output = []
for (league, round_), data in results.items():
    output.append({
        "league": league,
        "round": round_,
        "draws_0_0": data["draws_0_0"],
        "max_draws": 3  # prozatím fixně
    })

# Uložení do data.json
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(output, f, indent=2, ensure_ascii=False)
