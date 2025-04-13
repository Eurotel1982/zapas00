import requests
import json
from datetime import date, timedelta

API_KEY = "8bb57fb34476880013cbe2f37d283451"
headers = { "x-apisports-key": API_KEY }

# Sezóny, které chceme analyzovat (historie + současnost)
seasons = [2023, 2024, 2025]
results = {}

for season in seasons:
    url = f"https://v3.football.api-sports.io/fixtures?season={season}&status=FT"
    response = requests.get(url, headers=headers)
    fixtures = response.json().get("response", [])

    for match in fixtures:
        league = match.get("league", {})
        country = league.get("country", "Neznámý stát")
        league_name = league.get("name", "Neznámá liga")
        round_ = league.get("round", "Neznámé kolo")
        goals = match.get("goals", {})

        if goals.get("home") == 0 and goals.get("away") == 0:
            key = (country + " – " + league_name, round_)
            if key not in results:
                results[key] = 0
            results[key] += 1

# Najdeme maximum 0:0 v rámci každé ligy (napříč koly)
max_draws_per_league = {}
for (league, round_), draws in results.items():
    if league not in max_draws_per_league:
        max_draws_per_league[league] = draws
    else:
        max_draws_per_league[league] = max(max_draws_per_league[league], draws)

# Výpočet počtu 0:0 v aktuálním kole (pouze pro dnešní den)
today = date.today().isoformat()
url_today = f"https://v3.football.api-sports.io/fixtures?date={today}&status=FT"
response_today = requests.get(url_today, headers=headers)
fixtures_today = response_today.json().get("response", [])

current_results = {}

for match in fixtures_today:
    league = match.get("league", {})
    country = league.get("country", "Neznámý stát")
    league_name = league.get("name", "Neznámá liga")
    round_ = league.get("round", "Neznámé kolo")
    goals = match.get("goals", {})

    if goals.get("home") == 0 and goals.get("away") == 0:
        key = (country + " – " + league_name, round_)
        if key not in current_results:
            current_results[key] = 0
        current_results[key] += 1

# Sestavení finálního výstupu
output = []
for (league, round_), draws in current_results.items():
    max_draws = max_draws_per_league.get(league, 3)
    output.append({
        "league": league,
        "round": round_,
        "draws_0_0": draws,
        "max_draws": max_draws
    })

# Uložení do data.json
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(output, f, indent=2, ensure_ascii=False)
