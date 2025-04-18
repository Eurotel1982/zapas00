import requests
import json
from datetime import datetime, timedelta
import os

API_KEY = os.getenv("PERSONAL_TOKEN")

today = datetime.utcnow().date()
start_date = today - timedelta(days=3)  # 4 dny včetně dneška

url = f"https://v3.football.api-sports.io/fixtures?from={start_date}&to={today}"
headers = {
    "x-apisports-key": API_KEY
}

response = requests.get(url, headers=headers)
fixtures = response.json().get("response", [])

# --- KONEČNÉ VÝSLEDKY 0:0 ---
results = {}
for match in fixtures:
    if (match["goals"]["home"] == 0 and match["goals"]["away"] == 0 
        and match["fixture"]["status"]["short"] == "FT"):
        league = match["league"]["name"]
        round_ = match["league"].get("round", "")
        key = (league, round_)
        results[key] = results.get(key, 0) + 1

fulltime_output = []
for (league, round_), count in results.items():
    fulltime_output.append({
        "league": league,
        "round": round_,
        "draws_0_0": count
    })

# --- SÉRIE POLOČASŮ 0:0 ---
halftime_series = {}
for match in fixtures:
    if match["fixture"]["status"]["short"] != "FT":
        continue

    league = match["league"]["name"]
    round_ = match["league"].get("round", "")
    halftime_home = match["score"]["halftime"]["home"]
    halftime_away = match["score"]["halftime"]["away"]

    key = (league, round_)
    if key not in halftime_series:
        halftime_series[key] = []

    halftime_series[key].append((halftime_home == 0 and halftime_away == 0))

# Najdi max sérii 0:0 poločasů
halftime_output = []
for (league, round_), series in halftime_series.items():
    max_streak = 0
    current = 0
    for is_draw in series:
        if is_draw:
            current += 1
            max_streak = max(max_streak, current)
        else:
            current = 0
    halftime_output.append({
        "league": league,
        "round": round_,
        "max_halftime_0_0_series": max_streak
    })

# --- ULOŽ VÝSTUP ---
final_output = {
    "fulltime_draws": fulltime_output,
    "halftime_draws_series": halftime_output
}

with open("data.json", "w", encoding="utf-8") as f:
    json.dump(final_output, f, ensure_ascii=False, indent=2)
