import requests

# ---------------- AQICN API ----------------

AQICN_API_KEY = "YOUR_API_KEY"

def fetch_aqi_data(city="chennai"):

    url = f"https://api.waqi.info/feed/{city}/?token={AQICN_API_KEY}"

    response = requests.get(url)

    data = response.json()

    return data