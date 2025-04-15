import requests
import json
from datetime import datetime, timedelta
import os

API_KEY = os.getenv("PERSONAL_TOKEN")

# Rozsah posledních 4 dnů (včetně dneška)
today = datetime.utcnow().date()
start_date = today - timedelta(days=3)

results = {}

# Pro každý den v rozsahu
for i in range(4):
    date = start_date + timedelta(days=i)
    url = f"https://v3.football.api-sports.io/fixtures?date={date}"

    headers = {
        "x-apisports-key": API_KEY
    }

    response = requests.get(url, headers=headers)
    fixtures = response.json().get("response", [])

    for match in fixtures:
        if (match["goals"]["home"] == 0 and
            match["goals"]["away"] == 0 and
            match["fixture"]["status"]["short"] == "FT"):

            league_name = match["league"]["name"]
            round_name = match["league"].get("round", "")

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
