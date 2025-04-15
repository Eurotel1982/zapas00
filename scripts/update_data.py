import requests
import json
from datetime import datetime, timedelta
import os

API_KEY = os.getenv("PERSONAL_TOKEN")

# Dnešní datum a tři dny zpět
today = datetime.utcnow().date()
start_date = today - timedelta(days=3)

# URL s filtrem podle data
url = f"https://v3.football.api-sports.io/fixtures?from={start_date}&to={today}"
headers = {
    "x-apisports-key": API_KEY
}

response = requests.get(url, headers=headers)
fixtures = response.json().get("response", [])

# >>> ULOŽENÍ všech stažených zápasů pro ladění
with open("all_matches.json", "w", encoding="utf-8") as f:
    json.dump(fixtures, f, ensure_ascii=False, indent=2)

# >>> Filtruj výsledky 0:0 podle soutěže a kola
results = {}
for match in fixtures:
    if (
        match["goals"]["home"] == 0 and
        match["goals"]["away"] == 0 and
        match["fixture"]["status"]["short"] == "FT"
    ):
        league_name = match["league"]["name"]
        round_name = match["league"].get("round", "")
        key = (league_name, round_name)

        if key not in results:
            results[key] = 0
        results[key] += 1

# >>> Převod do výstupní struktury
output = []
for (league_name, round_name), count in results.items():
    output.append({
        "league": league_name,
        "round": round_name,
        "draws_0_0": count
    })

# >>> Ulož jako data.json
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)
