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

# Sběr sérií poločasových remíz v rámci jednoho kola
halftime_series = {}
for match in fixtures:
    if match["fixture"]["status"]["short"] == "FT":
        league = match["league"]["name"]
        round_name = match["league"].get("round", "")
        halftime = match.get("score", {}).get("halftime", {})
        if halftime.get("home") == 0 and halftime.get("away") == 0:
            key = (league, round_name)
            halftime_series.setdefault(key, []).append(1)
        else:
            halftime_series.setdefault(key, []).append(0)

# Zjisti max. sérii 0:0 poločasů v řadě
halftime_streaks = {}
for key, series in halftime_series.items():
    max_streak = streak = 0
    for val in series:
        if val == 1:
            streak += 1
            max_streak = max(max_streak, streak)
        else:
            streak = 0
    if max_streak > 0:
        halftime_streaks[key] = max_streak

# Výstup pro JSON
output = {
    "fulltime_draws": [
        {"league": league, "round": round_name, "draws_0_0": count}
        for (league, round_name), count in fulltime_results.items()
    ],
    "halftime_draws_series": [
        {"league": league, "round": round_name, "series_0_0": streak}
        for (league, round_name), streak in halftime_streaks.items()
    ]
}

# Uložení
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)
