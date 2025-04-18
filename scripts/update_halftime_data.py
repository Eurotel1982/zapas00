import requests
import os
from datetime import datetime, timedelta
import json

API_KEY = os.getenv("PERSONAL_TOKEN")

today = datetime.utcnow().date()
start_date = today - timedelta(days=3)

url = f"https://v3.football.api-sports.io/fixtures?from={start_date}&to={today}"
headers = { "x-apisports-key": API_KEY }

response = requests.get(url, headers=headers)
data = response.json()

# Vypiš do konzole pro GitHub Actions
print(json.dumps(data, indent=2, ensure_ascii=False))
