import requests
import json
from datetime import datetime, timedelta
import os

API_KEY = os.getenv("PERSONAL_TOKEN")

today = datetime.utcnow().date()
days_back = 3
from_date = today - timedelta(days=days_back)
to_date = today

url = f"https://v3.football.api-sports.io/fixtures?from={from_date}&to={to_date}"
headers = { "x-apisports-key": API_KEY }

response = requests.get(url, headers=headers)
data = response.json()

# >>> LADĚNÍ – výpis celého výstupu z API (všechny zápasy)
print("=== LADĚNÍ: Získaná data z API ===")
print(json.dumps(data, indent=2, ensure_ascii=False))

# >>> Zatím NEUKLÁDÁME do souboru, jen ladíme výstup
