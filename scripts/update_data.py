import requests
import json
from datetime import datetime, timedelta
from collections import defaultdict

# API klíč
API_KEY = "8bb57fb34476880013cbe2f37d283451"
URL = "https://v3.football.api-sports.io/fixtures"

# Dny, které bereme v potaz (poslední 4 včetně dneška)
today = datetime.utcnow().date()
start_date = today - timedelta(days=3)
end_date = today

# Připravíme požadavek
params = {
    "from": start_date.isoformat(),
    "to": end_date.isoformat()
}
headers = {
    "x-apisports-key": API_KEY,
    "accept": "application/json"
}

# Volání API
response = requests.get(URL, headers=headers, params=params)
fixtures = response.json().get("response", [])

# Filtrování 0:0 zápasů, které skončily
zero_zero_fixtures = [
    f for f in fixtures
    if f["goals"]["home"] == 0 and f["goals"]["away"] == 0 and f["fixture"]["status"]["short"] == "FT"
]

# Seskupíme zápasy podle ligy a kola
summary = defaultdict(lambda: {"league": "", "round": "", "count_0_0": 0})

for f in zero_zero_fixtures:
    league_id = f["league"]["id"]
    league_name = f["league"]["name"]
    round_name = f["league"]["round"]

    key = (league_id, round_name)
    summary[key]["league"] = league_name
    summary[key]["round"] = round_name
    summary[key]["count_0_0"] += 1

# Převedeme do seznamu a uložíme
output_data = []

for (league_id, round_name), data in summary.items():
    output_data.append({
        "league_id": league_id,
        "league": data["league"],
        "round": data["round"],
        "count_0_0": data["count_0_0"]
    })

# Výstupní soubor
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(output_data, f, ensure_ascii=False, indent=2)
