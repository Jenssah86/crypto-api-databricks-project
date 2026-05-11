# api_connector.py

# Deze code haalt de prijzen van een aantal cryptocurrencies op van de CoinGecko API en slaat deze op in een CSV bestand, 
# zodat we offline kunnen werken.

import requests
import pandas as pd
from datetime import datetime, timezone
import os

# We gebruiken de CoinGecko API om de prijzen van een aantal cryptocurrencies op te halen.
coins = ["bitcoin", "ethereum", "ripple", "solana"]
BASE_URL = "https://api.coingecko.com/api/v3"

# We zetten de data van de afgelopen 90 dagen in een CSV bestand, zodat we offline kunnen werken.
all_rows = []

# We halen de prijzen van de afgelopen 90 dagen op voor elke cryptocurrency en slaan deze op in een lijst van dictionaries, 
# die we later omzetten naar een DataFrame en opslaan als CSV.
for coin in coins:
    print("Fetching:", coin)
    url = f"{BASE_URL}/coins/{coin}/market_chart?vs_currency=eur&days=90" # Endpoint van de CoinGecko API om de prijzen van de afgelopen 90 dagen op te halen.
    resp = requests.get(url)
    data = resp.json()

    for p in data["prices"]:
        dt = datetime.fromtimestamp(p[0] / 1000, tz=timezone.utc) # We zetten de timestamp om naar een datetime object in UTC tijdzone.
        
        all_rows.append({
            "coin_id": coin,
            "price_timestamp": dt.replace(minute=0, second=0, microsecond=0),
            "price": p[1]
        })

# We zetten de lijst van dictionaries om naar een DataFrame en slaan deze op als CSV bestand.
df = pd.DataFrame(all_rows)

# We maken een map "bronze" aan als deze nog niet bestaat en slaan het CSV bestand op in deze map.
os.makedirs("bronze", exist_ok=True)

# We gebruiken een timestamp in de bestandsnaam, zodat we meerdere versies van het bestand kunnen opslaan 
# zonder dat ze elkaar overschrijven.
timestamp_str = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
df.to_csv(f"bronze/offline_coingecko_prices_{timestamp_str}.csv", index=False)

# We printen een bericht om aan te geven dat het bestand is opgeslagen.
print(f"Saved /bronze/offline_coingecko_prices_{timestamp_str}.csv")
