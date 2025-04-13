import requests
import json
from datetime import date

API_KEY = "8bb57fb34476880013cbe2f37d283451"
headers = {"x-apisports-key": API_KEY}

# Pomocná funkce pro získání zápasů pro daný rok
def get_fixtures_for_season(season):
    url = f"https://v3.football.api-sports.io/fixtures?season={season}&status=FT"
    response = requests.get(url, headers=headers)
    return response.json().get("response", [])

# Získání aktuálních zápasů (pro daný den)
today = date.today().isoformat()
url_today = f"https://v3.football.api-sports.io/fixtures?date={today}"
fixtures_today = requests.get(url_today, headers=headers).json().get("response", [])

# Získání historických dat pro sezóny 2023 a 2024
fixtures_2023 = get_fixtures_for_season(2023)
fixtures_2024 = get_fixtures_for_season(2024)

# Pomocná funkce pro výpočet maximálních 0:0 pro každou ligu a kolo
def calculate_max_zeros(fixtures):
    stats = {}
    for match in fixtures:
        if match["goals"]["home"] == 0 and match["goals"]["away"] == 0:
            league = match["league"]["name"]
            round_ = match["league"]["round"]
            key = (league, round_)
            stats[key] = stats.get(key, 0) + 1

    # Najdeme maximum pro každou ligu napříč koly
    max_draws_per_league = {}
    for (league, round_), count in stats.items():
        if league not in max_draws_per_league or count > max_draws_per_league[league]:
            max_draws_per_league[league] = count
    return max_draws_per_league

# Spočítáme historická maxima
max_2023 = calculate_max_zeros(fixtures_2023)
max_2024 = calculate_max_zeros(fixtures_2024)

# Sloučíme obě sezóny
historical_max = {}
for league in set(list(max_2023.keys()) + list(max_2024.keys())):
    historical_max[league] = max(max_2023.get(league, 0), max_2024.get(league, 0))

# Výpočet pro aktuální den
results = {}
for match in fixtures_today:
    if match["fixture"]["status"]["short"] != "FT":
        continue

    league = match["league"]["name"]
    round_ = match["league"]["round"]
    goals = match["goals"]

    key = (league, round_)
    if key not in results:
        results[key] = {"draws_0_0": 0}

    if goals["home"] == 0 and goals["away"] == 0:
        results[key]["draws_0_0"] += 1

# Převod do výstupní struktury
output = []
for (league, round_), data in results.items():
    output.append({
        "league": league,
        "round": round_,
        "draws_0_0": data["draws_0_0"],
        "max_draws": historical_max.get(league, data["draws_0_0"])  # fallback = aktuální počet
    })

# Uložení do JSON
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(output, f, indent=2, ensure_ascii=False)
