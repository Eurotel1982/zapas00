
import requests
import json

API_KEY = "8bb57fb34476880013cbe2f37d283451"
headers = {
    "x-apisports-key": API_KEY
}

def get_active_leagues():
    url = "https://v3.football.api-sports.io/leagues?current=true"
    response = requests.get(url, headers=headers)
    data = response.json().get("response", [])
    return [league["league"]["id"] for league in data]

def get_current_round(league_id):
    url = f"https://v3.football.api-sports.io/fixtures/rounds?league={league_id}&season=2023&current=true"
    response = requests.get(url, headers=headers)
    rounds = response.json().get("response", [])
    return rounds[0] if rounds else None

def get_fixtures(league_id, round_name):
    url = f"https://v3.football.api-sports.io/fixtures?league={league_id}&season=2023&round={round_name}"
    response = requests.get(url, headers=headers)
    return response.json().get("response", [])

def process_data():
    leagues = get_active_leagues()
    results = []

    for league_id in leagues:
        round_name = get_current_round(league_id)
        if not round_name:
            continue

        fixtures = get_fixtures(league_id, round_name)
        draws = 0
        total = 0
        remaining = 0
        league_name = ""
        round_number = round_name

        for match in fixtures:
            league_name = match["league"]["name"]
            status = match["fixture"]["status"]["short"]
            goals = match["goals"]
            total += 1

            if status == "FT":
                if goals["home"] == 0 and goals["away"] == 0:
                    draws += 1
            elif status in ("NS", "TBD"):
                remaining += 1

        results.append({
            "league": league_name,
            "round": round_number,
            "draws_0_0": draws,
            "max_draws": draws,
            "remaining": remaining
        })

    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    process_data()
