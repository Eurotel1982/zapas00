
import requests
import json
from collections import defaultdict
from datetime import datetime

API_KEY = "8bb57fb34476880013cbe2f37d283451"
HEADERS = {"x-apisports-key": API_KEY}
BASE_URL = "https://v3.football.api-sports.io"

SEASONS = [2023, 2024, 2025]

def get_all_leagues():
    response = requests.get(f"{BASE_URL}/leagues", headers=HEADERS)
    leagues = response.json().get("response", [])
    return [
        {
            "id": league["league"]["id"],
            "name": league["league"]["name"],
            "country": league["country"]["name"]
        }
        for league in leagues
        if league["seasons"][-1]["year"] in SEASONS
    ]

def get_fixtures(league_id, season):
    fixtures = []
    page = 1
    while True:
        url = f"{BASE_URL}/fixtures?league={league_id}&season={season}&status=FT&page={page}"
        response = requests.get(url, headers=HEADERS)
        data = response.json().get("response", [])
        if not data:
            break
        fixtures.extend(data)
        page += 1
    return fixtures

def process_fixtures(fixtures):
    counts = defaultdict(lambda: defaultdict(int))
    for f in fixtures:
        league_name = f["league"]["name"]
        round_name = f["league"]["round"]
        goals = f["goals"]
        if goals["home"] == 0 and goals["away"] == 0:
            counts[league_name][round_name] += 1
    max_per_league = {
        league: max(rounds.values()) for league, rounds in counts.items()
    }
    return max_per_league

def get_current_rounds():
    url = f"{BASE_URL}/fixtures?next=300"
    response = requests.get(url, headers=HEADERS)
    fixtures = response.json().get("response", [])
    current_data = {}
    for f in fixtures:
        league = f["league"]["name"]
        country = f["league"]["country"]
        round_ = f["league"]["round"]
        key = (league, round_)
        if key not in current_data:
            current_data[key] = {
                "league": league,
                "country": country,
                "round": round_,
                "draws_00_current": 0,
                "matches_remaining": 0
            }
        if f["fixture"]["status"]["short"] == "FT":
            goals = f["goals"]
            if goals["home"] == 0 and goals["away"] == 0:
                current_data[key]["draws_00_current"] += 1
        else:
            current_data[key]["matches_remaining"] += 1
    return current_data

def main():
    print("Stahuji seznam lig...")
    leagues = get_all_leagues()

    print("Stahuji historické zápasy...")
    all_fixtures = []
    for league in leagues:
        for season in SEASONS:
            fixtures = get_fixtures(league["id"], season)
            all_fixtures.extend(fixtures)

    print("Zpracovávám historická data...")
    max_draws = process_fixtures(all_fixtures)

    print("Načítám aktuální zápasy...")
    current = get_current_rounds()

    print("Generuji výstup...")
    output = []
    for (league, round_), values in current.items():
        output.append({
            "league": values["league"],
            "country": values["country"],
            "round": values["round"],
            "draws_00_current": values["draws_00_current"],
            "draws_00_max": max_draws.get(league, 0),
            "matches_remaining": values["matches_remaining"]
        })

    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print("Hotovo! Soubor data.json byl vytvořen.")

if __name__ == "__main__":
    main()
