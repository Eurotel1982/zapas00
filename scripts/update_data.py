
import requests
import json
from collections import defaultdict
from datetime import datetime, timedelta

API_KEY = "8bb57fb34476880013cbe2f37d283451"
HEADERS = {"x-apisports-key": API_KEY}
BASE_URL = "https://v3.football.api-sports.io"

def get_fixture_range():
    today = datetime.utcnow().date()
    weekday = today.weekday()
    start_delta = weekday - 4 if weekday >= 4 else -(3 + weekday)
    start_date = today + timedelta(days=start_delta)
    end_date = start_date + timedelta(days=3)
    return start_date.isoformat(), end_date.isoformat()

def fetch_fixtures(start_date, end_date):
    url = f"{BASE_URL}/fixtures?season=2024&from={start_date}&to={end_date}"
    response = requests.get(url, headers=HEADERS)
    return response.json().get("response", [])

def process_fixtures(fixtures):
    results = defaultdict(lambda: {"draws_0_0": 0, "matches": 0})
    for match in fixtures:
        league = match["league"]["name"]
        round_ = match["league"]["round"]
        goals = match["goals"]
        status = match["fixture"]["status"]["short"]

        if status != "FT":
            continue

        key = (league, round_)
        results[key]["matches"] += 1
        if goals["home"] == 0 and goals["away"] == 0:
            results[key]["draws_0_0"] += 1

    return results

def get_latest_rounds(results):
    current = {}
    for (league, round_), data in results.items():
        if league not in current or int(data["matches"]) > int(current[league]["matches"]):
            current[league] = {
                "league": league,
                "round": round_,
                "draws_00_current": data["draws_0_0"],
                "matches_remaining": 0,
                "draws_00_max": data["draws_0_0"]
            }
    return list(current.values())

def main():
    start_date, end_date = get_fixture_range()
    print(f"Načítám zápasy od {start_date} do {end_date}...")
    fixtures = fetch_fixtures(start_date, end_date)
    print(f"Získáno {len(fixtures)} zápasů.")

    results = process_fixtures(fixtures)
    latest = get_latest_rounds(results)

    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(latest, f, indent=2, ensure_ascii=False)

    print("Aktualizace dokončena.")

if __name__ == "__main__":
    main()
