import requests
import json
from datetime import datetime, timedelta
import pytz

API_KEY = "8bb57fb34476880013cbe2f37d283451"
headers = {
    "x-apisports-key": API_KEY
}

# Výpočet časového rozsahu (poslední 4 dny včetně dnešního)
today = datetime.now(pytz.UTC).date()
start_date = today - timedelta(days=3)
end_date = today

results = {}

for i in range((end_date - start_date).days + 1):
    date = start_date + timedelta(days=i)
    print(f"Zpracovávám datum: {date}")
    url = f"https://v3.football.api-sports.io/fixtures?date={date}"
    response = requests.get(url, headers=headers)
    fixtures = response.json().get("response", [])

    for match in fixtures:
        if match["fixture"]["status"]["short"] != "FT":
            continue

        league_raw = match.get("league")
        if isinstance(league_raw, dict):
            country_raw = league_raw.get("country")
            if isinstance(country_raw, dict):
                country = country_raw.get("name", "Neznámý stát")
            else:
                country = "Neznámý stát"
            league_name = f'{country} - {league_raw.get("name", "Neznámá liga")}'
        else:
            country = "Neznámý stát"
            league_name = f'{country} - {league_raw}'

        round_ = match["league"].get("round", "Neznámé kolo")
        goals = match.get("goals", {})

        key = (league_name, round_)
        if key not in results:
            results[key] = {"draws_0_0": 0, "matches": 0}

        results[key]["matches"] += 1
        if goals.get("home") == 0 and goals.get("away") == 0:
            results[key]["draws_0_0"] += 1

# Převod na výstupní strukturu
output = []
for (league, round_), data in results.items():
    output.append({
        "league": league,
        "round": round_,
        "draws_0_0": data["draws_0_0"],
        "max_draws": 3
    })

# Uložení do JSON
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)