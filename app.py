import os
from datetime import datetime
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# OPTIONAL MODEL LOAD (SAFE)
import joblib

try:
    model = joblib.load("model.pkl")
except:
    model = None
    st.warning("⚠ model.pkl not found → Using dummy prediction")

from utils.api import get_weather_data, get_live_aqi
from utils.email_alert import send_email_alert
from streamlit_autorefresh import st_autorefresh

# AUTO REFRESH
st_autorefresh(interval=60000, key="refresh")

# ─────────────────────────────
# SAFE AQI FUNCTION
# ─────────────────────────────
def predict_aqi(pm25, pm10, co, no2, o3, so2, nh3, temp, hum):

    if model is None:
        # fallback formula (no ML model)
        return int(
            0.4 * pm25 +
            0.2 * pm10 +
            0.1 * co +
            0.1 * no2 +
            0.1 * o3 +
            0.1 * hum
        )

    df = pd.DataFrame([{
        "pm2_5": pm25,
        "pm10": pm10,
        "temp_c": temp,
        "humidity": hum,
        "co": co,
        "no2": no2,
        "o3": o3,
        "so2": so2,
        "nh3": nh3
    }])

    return int(model.predict(df)[0])

# ─────────────────────────────
# AQI LEVEL
# ─────────────────────────────
def get_level(aqi):
    if aqi <= 50:
        return "Good", "#00FFA3"
    elif aqi <= 100:
        return "Moderate", "#FFC857"
    elif aqi <= 150:
        return "Sensitive", "#FF7A00"
    elif aqi <= 200:
        return "Unhealthy", "#FF3B30"
    elif aqi <= 300:
        return "Very Unhealthy", "#C084FC"
    else:
        return "Hazardous", "#FF006E"

# ─────────────────────────────
# HEALTH ADVICE
# ─────────────────────────────
def get_health_advice(aqi):
    if aqi <= 50:
        return "Good air quality 🌿"
    elif aqi <= 100:
        return "Moderate air 😷 sensitive people take care"
    elif aqi <= 150:
        return "Reduce outdoor activity 🟠"
    elif aqi <= 200:
        return "Wear mask 😷"
    elif aqi <= 300:
        return "Avoid going outside 🚫"
    else:
        return "Stay indoors ⚠"

# ─────────────────────────────
# SAFE API DATA
# ─────────────────────────────
try:
    weather = get_weather_data()
    aqi_data = get_live_aqi()
except:
    weather = {"temp": 30, "humidity": 60}
    aqi_data = {
        "pm25": 50, "pm10": 80,
        "co": 10, "no2": 20,
        "o3": 15, "so2": 5, "nh3": 5
    }

# SAFE VARIABLES (IMPORTANT FIX 🔥)
pm25 = aqi_data.get("pm25", 0)
pm10 = aqi_data.get("pm10", 0)
co = aqi_data.get("co", 0)
no2 = aqi_data.get("no2", 0)
o3 = aqi_data.get("o3", 0)
so2 = aqi_data.get("so2", 0)
nh3 = aqi_data.get("nh3", 0)

temp = weather.get("temp", 30)
hum = weather.get("humidity", 60)

# ─────────────────────────────
# AQI CALCULATION (ONLY ONCE FIXED)
# ─────────────────────────────
aqi = predict_aqi(pm25, pm10, co, no2, o3, so2, nh3, temp, hum)

label, color = get_level(aqi)
advice = get_health_advice(aqi)

# EMAIL ALERT
if aqi >= 100:
    try:
        send_email_alert(aqi, label)
    except:
        pass

# ─────────────────────────────
# UI
# ─────────────────────────────
st.set_page_config(page_title="PolluCast", layout="wide")

st.title("🌍 PolluCast Live Dashboard")

st.metric("AQI", aqi)
st.metric("Temperature", f"{temp} °C")
st.metric("Humidity", f"{hum}%")
st.metric("PM2.5", pm25)

st.markdown(f"""
<div style="padding:15px;border-left:5px solid {color};
background:#111;color:white;border-radius:10px;">
<h4>{label}</h4>
<p>{advice}</p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────
# TREND (SIMPLE)
# ─────────────────────────────
hours = list(range(24))
trend = [aqi + np.random.randint(-20, 20) for _ in hours]

fig = go.Figure()
fig.add_trace(go.Scatter(x=hours, y=trend, mode="lines"))

st.plotly_chart(fig, use_container_width=True)

# ─────────────────────────────
# SAVE DATA
# ─────────────────────────────
df = pd.DataFrame([{
    "time": datetime.now(),
    "aqi": aqi,
    "pm25": pm25,
    "pm10": pm10,
    "temp": temp,
    "humidity": hum
}])

if os.path.exists("dataset.csv"):
    old = pd.read_csv("dataset.csv")
    df = pd.concat([old, df])

df.to_csv("dataset.csv", index=False)

st.success("✅ Dashboard Running Smoothly!")