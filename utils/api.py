import requests
import streamlit as st

OPENWEATHER_API_KEY = "OPENWEATHER_API_KEY"
AQICN_TOKEN = "AQICN_TOKEN"

CITY = "Chennai"


# ─────────────────────────────────────────────
# WEATHER DATA
# ─────────────────────────────────────────────

def get_weather_data():

    try:

        url = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={OPENWEATHER_API_KEY}&units=metric"

        response = requests.get(url)

        data = response.json()

        return {
            "temp": data["main"]["temp"],
            "humidity": data["main"]["humidity"]
        }

    except:

        return {
            "temp": 30,
            "humidity": 60
        }


# ─────────────────────────────────────────────
# LIVE AQI DATA
# ─────────────────────────────────────────────

def get_live_aqi():

    try:

        url = f"https://api.waqi.info/feed/{CITY}/?token={AQICN_TOKEN}"

        response = requests.get(url)

        data = response.json()

        iaqi = data["data"]["iaqi"]

        return {

            "pm25": iaqi.get("pm25", {}).get("v", 50),

            "pm10": iaqi.get("pm10", {}).get("v", 80),

            "co": iaqi.get("co", {}).get("v", 500),

            "no2": iaqi.get("no2", {}).get("v", 20),

            "o3": iaqi.get("o3", {}).get("v", 30),

            "so2": iaqi.get("so2", {}).get("v", 10)
        }

    except:

        return {

            "pm25": 80,

            "pm10": 120,

            "co": 800,

            "no2": 40,

            "o3": 30,

            "so2": 20
        }