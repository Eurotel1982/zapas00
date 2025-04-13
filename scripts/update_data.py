
import requests
import json
from collections import defaultdict

API_KEY = "8bb57fb34476880013cbe2f37d283451"
HEADERS = {"x-apisports-key": API_KEY}
BASE_URL = "https://v3.football.api-sports.io"

def fetch_fixtures():
    url = f"{BASE_URL}/fixtures?season=2024&status=FT&next=500"
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

def get_current_rounds(results):
    current = {}
    for (league, round_), data in results.items():
        if league not in current or int(data["matches"]) > int(current[league]["matches"]):
            current[league] = {
                "league": league,
                "round": round_,
                "draws_0_0": data["draws_0_0"],
                "matches": data["matches"]
            }
    return list(current.values())

def main():
    print("Stahuji zápasy...")
    fixtures = fetch_fixtures()
    print(f"Načteno zápasů: {len(fixtures)}")

    print("Zpracovávám výsledky...")
    results = process_fixtures(fixtures)

    print("Identifikuji aktuální kola...")
    current = get_current_rounds(results)

    print("Ukládám data do data.json...")
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(current, f, indent=2, ensure_ascii=False)

    print("Hotovo!")

if __name__ == "__main__":
    main()
