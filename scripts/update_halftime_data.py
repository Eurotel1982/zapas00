import requests
import json
from datetime import datetime, timedelta
import os

API_KEY = os.getenv("PERSONAL_TOKEN")

# Poslední 4 dny včetně dneška
today = datetime.utcnow().date()
start_date = today - timedelta(days=3)

url = f"https://v3.football.api-sports.io/fixtures?from={start_date}&to={today}"
headers = { "x-apisports-key": API_KEY }

response = requests.get(url, headers=headers)
fixtures = response.json().get("response", [])

# >>> DEBUG výpis do souboru
with open("debug_halftime.json", "w", encoding="utf-8") as debug_file:
    json.dump(fixtures, debug_file, ensure_ascii=False, indent=2)

# >>> VÝPOČET: Série 0:0 v poločase v jednom kole
series = {}
for match in fixtures:
    if match["status"]["short"] != "FT":
        continue

    halftime = match.get("score", {}).get("halftime", {})
    if halftime.get("home") != 0 or halftime.get("away") != 0:
        continue

    league_name = match["league"]["name"]
    round_name = match["league"].get("round", "")
    key = (league_name, round_name)

    if key not in series:
        series[key] = 0
    series[key] += 1

# >>> Filtruj jen série s alespoň 2 poločasy 0:0 v řadě
output_series = []
for (league, round_), count in series.items():
    if count >= 2:
        output_series.append({
            "league": league,
            "round": round_,
            "draws_0_0_halftime_in_a_row": count
        })

# >>> Sloučení s fulltime daty (zachovej strukturu JSONu)
try:
    with open("data.json", "r", encoding="utf-8") as f:
        current_data = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    current_data = {}

current_data["halftime_draws_series"] = output_series

# >>> Ulož výstup
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(current_data, f, ensure_ascii=False, indent=2)
