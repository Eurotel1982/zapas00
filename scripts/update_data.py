import requests
import json
from datetime import datetime, timedelta
import os

API_KEY = os.getenv("PERSONAL_TOKEN")

# Dny zpět
today = datetime.utcnow().date()
days_back = 3
dates = [(today - timedelta(days=i)).isoformat() for i in range(days_back + 1)]

# Sběr všech zápasů
fixtures = []
for date in dates:
    url = f"https://v3.football.api-sports.io/fixtures?date={date}"
    headers = {"x-apisports-key": API_KEY}
    response = requests.get(url, headers=headers)
    daily = response.json().get("response", [])
    fixtures.extend(daily)

# Počet remíz 0:0 na konci zápasu (fulltime)
fulltime_results = {}
for match in fixtures:
    if (
        match["goals"]["home"] == 0
        and match["goals"]["away"] == 0
        and match["fixture"]["status"]["short"] == "FT"
    ):
        league = match["league"]["name"]
        round_name = match["league"].get("round", "")
        key = (league, round_name)
        fulltime_results[key] = fulltime_results.get(key, 0) + 1

# Výstup pro JSON
output = {
    "fulltime_draws": 
        {"league": league, "round": round_name, "draws_0_0": count}
        for (league, round_name), count in fulltime_results.items()
    
# Uložení
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)
