import requests
import json
from datetime import datetime, timedelta
import os

API_KEY = os.getenv("PERSONAL_TOKEN")

# Dny od dneška zpět
today = datetime.utcnow().date()
start_date = today - timedelta(days=3)

url = f"https://v3.football.api-sports.io/fixtures?from={start_date}&to={today}"

headers = {
    "x-apisports-key": API_KEY
}

response = requests.get(url, headers=headers)
fixtures = response.json().get("response", [])

# Uložení všech zápasů pro ladění
with open("all_matches.json", "w", encoding="utf-8") as f:
    json.dump(fixtures, f, ensure_ascii=False, indent=2)

# Počítání sérií 0:0 v poločase
results = {}

for match in fixtures:
    if match["fixture"]["status"]["short"] != "FT":
        continue

    halftime_goals = match.get("goals", {}).get("halftime", {})
    if halftime_goals.get("home") == 0 and halftime_goals.get("away") == 0:
        league = match["league"]["name"]
        round_ = match["league"].get("round", "")
        key = (league, round_)

        if key not in results:
            results[key] = 1
        else:
            results[key] += 1

# Výstupní pole (zatím bez podmínky >= 2)
output = []
for (league, round_), count in results.items():
    output.append({
        "league": league,
        "round": round_,
        "halftime_0_0_series": count
    })

# Vložení do data.json (do existujícího klíče)
try:
    with open("data.json", "r", encoding="utf-8") as f:
        data = json.load(f)
except FileNotFoundError:
    data = {}

data["halftime_draws_series"] = output

with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
