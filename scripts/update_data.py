
import requests
import json
from datetime import datetime, timedelta

API_KEY = "8bb57fb34476880013cbe2f37d283451"
headers = {
    "x-apisports-key": API_KEY
}

# Získání dat pro dnešek a včerejšek
today = datetime.utcnow().date()
yesterday = today - timedelta(days=1)
url = f"https://v3.football.api-sports.io/fixtures?from={yesterday}&to={today}"

print("Spouštím update_data.py")
print(f"Načítám zápasy od {yesterday} do {today}...")

response = requests.get(url, headers=headers)
fixtures = response.json().get("response", [])

print(f"Získáno {len(fixtures)} zápasů.")
print("Zpracovávám výsledky...")

results = {}

for match in fixtures:
    league_raw = match.get("league", {})
    country_raw = league_raw.get("country", {})
    country = country_raw.get("name", "Neznámý stát") if isinstance(country_raw, dict) else "Neznámý stát"
    league_name = f"{country} – {league_raw.get('name', 'Neznámá liga')}"
    round_ = league_raw.get("round", "Neznámé kolo")
    goals = match.get("goals", {})
    status = match.get("fixture", {}).get("status", {}).get("short", "")

    if status != "FT":
        continue

    key = (league_name, round_)
    if key not in results:
        results[key] = {"draws_0_0": 0, "matches": 0}
    results[key]["matches"] += 1
    if goals.get("home") == 0 and goals.get("away") == 0:
        results[key]["draws_0_0"] += 1

output = []
for (league, round_), data in results.items():
    output.append({
        "league": league,
        "round": round_,
        "draws_0_0": data["draws_0_0"],
        "max_draws": 3  # zatím pevně nastaveno
    })

with open("data.json", "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print("Aktualizace dokončena.")
