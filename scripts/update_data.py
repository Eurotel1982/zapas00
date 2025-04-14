
import requests
import json
from datetime import datetime, timedelta

API_KEY = "8bb57fb34476880013cbe2f37d283451"

# Načti mapu lig a států
with open("league_map.json", "r", encoding="utf-8") as f:
    league_map = json.load(f)

# Dnešní datum a den zpět
today = datetime.utcnow().date()
yesterday = today - timedelta(days=1)

# URL s filtrem podle data
url = f"https://v3.football.api-sports.io/fixtures?from={yesterday}&to={today}"

headers = {
    "x-apisports-key": API_KEY
}

response = requests.get(url, headers=headers)
fixtures = response.json().get("response", [])

# Výsledky 0:0 podle lig
results = {}

for match in fixtures:
    league_id = str(match["league"]["id"])
    league_name = league_map.get(league_id, f"Neznámý stát - {match['league']['name']}")

    if match["goals"]["home"] == 0 and match["goals"]["away"] == 0 and match["fixture"]["status"]["short"] == "FT":
        if league_name not in results:
            results[league_name] = 1
        else:
            results[league_name] += 1

# Ulož jako data.json
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
