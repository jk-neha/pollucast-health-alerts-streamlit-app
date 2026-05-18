import os
from datetime import datetime

import joblib
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from streamlit_autorefresh import st_autorefresh

from utils.api import get_live_aqi, get_weather_data
from utils.email_alert import send_email_alert

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="PolluCast · Live",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)

st_autorefresh(interval=60_000, key="pollucast_refresh")

# ─────────────────────────────────────────────
# DARK MODE TOGGLE (FIXED)
# ─────────────────────────────────────────────
dark_mode = st.toggle("🌗 Dark Mode", value=True)

if dark_mode:
    BG = "#0E0F12"
    CARD = "#16181D"
    TEXT = "#F5F5F5"
    MUTED = "#A8A8A8"
    BORDER = "#2A2D35"
    GRID = "#222"
else:
    BG = "#F5F4F0"
    CARD = "#FFFFFF"
    TEXT = "#1A1916"
    MUTED = "#A8A49C"
    BORDER = "#E5E3DC"
    GRID = "#EDEBE4"

# ─────────────────────────────────────────────
# GLOBAL CSS (NOW RESPONSIVE TO THEME)
# ─────────────────────────────────────────────
st.markdown(f"""
<style>
.stApp {{
    background: {BG};
    color: {TEXT};
}}

[data-testid="metric-container"] {{
    background: {CARD} !important;
    border: 1px solid {BORDER} !important;
    border-radius: 16px !important;
}}

[data-testid="stSidebar"] {{
    background: {CARD} !important;
    border-right: 1px solid {BORDER} !important;
}}

[data-testid="stDataFrame"] {{
    background: {CARD} !important;
    border: 1px solid {BORDER} !important;
    border-radius: 12px;
}}

.stDownloadButton > button {{
    background: {TEXT} !important;
    color: {BG} !important;
}}

</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# MODEL
# ─────────────────────────────────────────────
@st.cache_resource
def load_model():
    return joblib.load("model.pkl")

model = load_model()

# ─────────────────────────────────────────────
# DATA
# ─────────────────────────────────────────────
try:
    weather = get_weather_data()
    aqi_data = get_live_aqi()
except:
    weather, aqi_data = {}, {}

pm25 = float(aqi_data.get("pm25", 50))
pm10 = float(aqi_data.get("pm10", 80))
co   = float(aqi_data.get("co", 400))
no2  = float(aqi_data.get("no2", 20))
o3   = float(aqi_data.get("o3", 25))
so2  = float(aqi_data.get("so2", 10))
nh3  = float(aqi_data.get("nh3", 5))
temp = float(weather.get("temp", 30))
hum  = float(weather.get("humidity", 60))

# ─────────────────────────────────────────────
# AQI MODEL (simple safe version kept)
# ─────────────────────────────────────────────
def predict_aqi():
    return int(pm25 * 0.8 + pm10 * 0.4 + co * 0.01)

aqi = predict_aqi()

def get_level(aqi):
    if aqi <= 50:
        return "Good", "#16A37F"
    elif aqi <= 100:
        return "Moderate", "#D4820A"
    elif aqi <= 150:
        return "Unhealthy", "#C45C2A"
    else:
        return "Hazardous", "#C0392B"

label, color = get_level(aqi)

# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
st.markdown(f"""
<h1 style="color:{TEXT}">🌍 PolluCast</h1>
<p style="color:{MUTED}">Live AQI Dashboard</p>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# METRICS
# ─────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)

c1.metric("AQI", aqi)
c2.metric("Category", label)
c3.metric("Temp", f"{temp}°C")
c4.metric("Humidity", f"{hum}%")

# ─────────────────────────────────────────────
# CHART (THEME FIXED)
# ─────────────────────────────────────────────
hours = list(range(24))
trend = [aqi + np.random.randint(-20, 20) for _ in hours]

fig = go.Figure()
fig.add_trace(go.Scatter(
    x=hours,
    y=trend,
    mode="lines",
    line=dict(color=color, width=3),
    fill="tozeroy",
    fillcolor="rgba(0,255,163,0.1)" if dark_mode else "rgba(0,0,0,0.05)"
))

fig.update_layout(
    paper_bgcolor=BG,
    plot_bgcolor=BG,
    font=dict(color=TEXT),
    xaxis=dict(gridcolor=GRID),
    yaxis=dict(gridcolor=GRID),
    height=300
)

st.plotly_chart(fig, use_container_width=True)

# ─────────────────────────────────────────────
# POLLUTANTS
# ─────────────────────────────────────────────
st.subheader("Pollutants")

cols = st.columns(4)
data = [("PM2.5", pm25), ("PM10", pm10), ("CO", co), ("NO2", no2)]

for i, (name, val) in enumerate(data):
    cols[i].metric(name, f"{val:.1f}")

# ─────────────────────────────────────────────
# ALERT
# ─────────────────────────────────────────────
st.info(f"Status: {label}")

if aqi > 100:
    try:
        send_email_alert(aqi, label)
    except:
        pass

# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown(f"""
<hr style="border:1px solid {BORDER}">
<p style="color:{MUTED}">PolluCast · Neha Project</p>
""", unsafe_allow_html=True)