import requests
import json
from datetime import datetime, timedelta
import os

API_KEY = os.getenv("PERSONAL_TOKEN")

# Dnešní datum a den zpět
today = datetime.utcnow().date()
yesterday = today - timedelta(days=1)

# URL s filtrem podle data
url = f"https://v3.football.api-sports.io/fixtures?from={yesterday}&to={today}"
headers = { "x-apisports-key": API_KEY }

response = requests.get(url, headers=headers)
fixtures = response.json().get("response", [])

# >>> LADĚNÍ – ulož všechna získaná data (pro kontrolu)
with open("all_matches.json", "w", encoding="utf-8") as debug_file:
    json.dump(fixtures, debug_file, ensure_ascii=False, indent=2)

# >>> Filtruj výsledky 0:0
results = {}
for match in fixtures:
    if match["goals"]["home"] == 0 and match["goals"]["away"] == 0 and match["fixture"]["status"]["short"] == "FT":
        league_name = match['league']['name']
        round_name = match['league'].get('round', '')
        key = (league_name, round_name)
        if key not in results:
            results[key] = 0
        results[key] += 1

# Výstupní struktura
output = []
for (league_name, round_name), count in results.items():
    output.append({
        "league": league_name,
        "round": round_name,
        "draws_0_0": count
    })

# Ulož jako data.json
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)
