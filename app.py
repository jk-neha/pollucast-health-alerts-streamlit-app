import os
from datetime import datetime
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import joblib
from utils.api import get_weather_data, get_live_aqi
from streamlit_autorefresh import st_autorefresh
from utils.email_alert import send_email_alert
# LOAD TRAINED MODEL
model = joblib.load("model.pkl")

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="PolluCast • Live Dashboard",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)
st_autorefresh(interval=60000, key="pollucastrefresh")
# ─────────────────────────────────────────────
# BLACK AESTHETIC CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=JetBrains+Mono:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at top left, rgba(0,255,170,0.06), transparent 25%),
        radial-gradient(circle at bottom right, rgba(0,140,255,0.05), transparent 25%),
        #050505;
    color: #F5F5F5;
}

#MainMenu,
footer,
header {
    visibility: hidden;
}

/* SIDEBAR */

[data-testid="stSidebar"] {
    background: rgba(10,10,10,0.97) !important;
    border-right: 1px solid rgba(255,255,255,0.06);
}

[data-testid="stSidebar"] label {
    color: #8E8E93 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 11px !important;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}

/* METRICS */

[data-testid="metric-container"] {
    background: rgba(18,18,18,0.72) !important;
    border: 1px solid rgba(255,255,255,0.06) !important;
    border-radius: 22px !important;
    padding: 24px !important;

    backdrop-filter: blur(12px);

    box-shadow:
        0 8px 32px rgba(0,0,0,0.45);

    transition: all 0.25s ease;
}

[data-testid="metric-container"]:hover {
    transform: translateY(-4px);
    border: 1px solid rgba(0,255,163,0.20) !important;
    box-shadow:
        0 0 20px rgba(0,255,163,0.08),
        0 10px 35px rgba(0,0,0,0.55);
}

[data-testid="stMetricLabel"] p {
    color: #8E8E93 !important;
    font-family: 'JetBrains Mono', monospace !important;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    font-size: 10px !important;
}

[data-testid="stMetricValue"] {
    color: white !important;
    font-size: 34px !important;
    font-weight: 700 !important;
}

/* BUTTONS */

.stDownloadButton > button {
    background: linear-gradient(
        135deg,
        #00FFA3,
        #00C2FF
    ) !important;

    color: black !important;
    border: none !important;
    border-radius: 14px !important;

    font-weight: 600 !important;

    transition: 0.25s ease;
}

.stDownloadButton > button:hover {
    transform: scale(1.03);
    box-shadow:
        0 0 25px rgba(0,255,163,0.25);
}

/* DATAFRAME */

[data-testid="stDataFrame"] {
    border-radius: 20px !important;
    overflow: hidden;
    border: 1px solid rgba(255,255,255,0.06) !important;
}

/* SCROLLBAR */

::-webkit-scrollbar {
    width: 6px;
}

::-webkit-scrollbar-track {
    background: #050505;
}

::-webkit-scrollbar-thumb {
    background: #222;
    border-radius: 20px;
}

::-webkit-scrollbar-thumb:hover {
    background: #444;
}

</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# AQI CALCULATION
# ─────────────────────────────────────────────
AQI_LEVELS = [
    (50, "Good", "#00FFA3"),
    (100, "Moderate", "#FFC857"),
    (150, "Sensitive", "#FF7A00"),
    (200, "Unhealthy", "#FF3B30"),
    (300, "Very Unhealthy", "#C084FC"),
    (500, "Hazardous", "#FF006E"),
]
FEATURE_COLUMNS = [
    "pm2_5","pm10","temp_c","humidity","co","no","no2","o3","so2","nh3",
    "AQI_PM25","AQI_PM10","AQI_Category",
    "hour","day","weekday","month",
    "pm2_5_3h_avg","pm10_3h_avg","co_3h_avg","no_3h_avg","no2_3h_avg",
    "o3_3h_avg","so2_3h_avg","nh3_3h_avg","temp_c_3h_avg","humidity_3h_avg",
    "pm2_5_24h_avg","pm10_24h_avg","co_24h_avg","no_24h_avg","no2_24h_avg",
    "o3_24h_avg","so2_24h_avg","nh3_24h_avg","temp_c_24h_avg","humidity_24h_avg",
    "pm2_5_lag_1h","pm2_5_lag_3h","pm2_5_lag_24h",
    "pm10_lag_1h","pm10_lag_3h","pm10_lag_24h",
    "co_lag_1h","co_lag_3h","co_lag_24h",
    "no_lag_1h","no_lag_3h","no_lag_24h",
    "no2_lag_1h","no2_lag_3h","no2_lag_24h",
    "o3_lag_1h","o3_lag_3h","o3_lag_24h",
    "so2_lag_1h","so2_lag_3h","so2_lag_24h",
    "nh3_lag_1h","nh3_lag_3h","nh3_lag_24h",
    "temp_c_lag_1h","temp_c_lag_3h","temp_c_lag_24h",
    "humidity_lag_1h","humidity_lag_3h","humidity_lag_24h",
    "AQI_lag_1h","AQI_lag_3h","AQI_lag_24h"
]
def predict_aqi(pm25, pm10, co, no2, o3, so2, nh3, temp, hum):

    input_data = {
        "pm2_5": pm25,
        "pm10": pm10,
        "temp_c": temp,
        "humidity": hum,
        "co": co,
        "no": 0,
        "no2": no2,
        "o3": o3,
        "so2": so2,
        "nh3": nh3,

        "AQI_PM25": pm25,
        "AQI_PM10": pm10,
        "AQI_Category": 1,

        "hour": 12,
        "day": 1,
        "weekday": 1,
        "month": 1,

        "pm2_5_3h_avg": pm25,
        "pm10_3h_avg": pm10,
        "co_3h_avg": co,
        "no_3h_avg": 0,
        "no2_3h_avg": no2,
        "o3_3h_avg": o3,
        "so2_3h_avg": so2,
        "nh3_3h_avg": nh3,
        "temp_c_3h_avg": temp,
        "humidity_3h_avg": hum,

        "pm2_5_24h_avg": pm25,
        "pm10_24h_avg": pm10,
        "co_24h_avg": co,
        "no_24h_avg": 0,
        "no2_24h_avg": no2,
        "o3_24h_avg": o3,
        "so2_24h_avg": so2,
        "nh3_24h_avg": nh3,
        "temp_c_24h_avg": temp,
        "humidity_24h_avg": hum,

        "pm2_5_lag_1h": pm25,
        "pm2_5_lag_3h": pm25,
        "pm2_5_lag_24h": pm25,

        "pm10_lag_1h": pm10,
        "pm10_lag_3h": pm10,
        "pm10_lag_24h": pm10,

        "co_lag_1h": co,
        "co_lag_3h": co,
        "co_lag_24h": co,

        "no_lag_1h": 0,
        "no_lag_3h": 0,
        "no_lag_24h": 0,

        "no2_lag_1h": no2,
        "no2_lag_3h": no2,
        "no2_lag_24h": no2,

        "o3_lag_1h": o3,
        "o3_lag_3h": o3,
        "o3_lag_24h": o3,

        "so2_lag_1h": so2,
        "so2_lag_3h": so2,
        "so2_lag_24h": so2,

        "nh3_lag_1h": nh3,
        "nh3_lag_3h": nh3,
        "nh3_lag_24h": nh3,

        "temp_c_lag_1h": temp,
        "temp_c_lag_3h": temp,
        "temp_c_lag_24h": temp,

        "humidity_lag_1h": hum,
        "humidity_lag_3h": hum,
        "humidity_lag_24h": hum,

        "AQI_lag_1h": 100,
        "AQI_lag_3h": 100,
        "AQI_lag_24h": 100,
    }

    df = pd.DataFrame([input_data])

    # FORCE SAME ORDER
    df = df[FEATURE_COLUMNS]

    prediction = model.predict(df)[0]

    return int(round(prediction))

def get_level(aqi):
    for limit, label, color in AQI_LEVELS:
        if aqi <= limit:
            return label, color
    return "Hazardous", "#FF006E"
def get_health_advice(aqi):

    if aqi <= 50:
        return "🟢 Air quality is good. Safe for outdoor activities."

    elif aqi <= 100:
        return "🟡 Moderate air quality. Sensitive people should take care."

    elif aqi <= 150:
        return "🟠 Sensitive groups should reduce outdoor exposure."

    elif aqi <= 200:
        return "🔴 Unhealthy air quality. Wear a mask outdoors."

    elif aqi <= 300:
        return "🟣 Very unhealthy conditions. Avoid outdoor activities."

    else:
        return "⚫ Hazardous air quality. Stay indoors and use air purification."

def save_live_data(pm25, pm10, co, no2, o3, so2, nh3, temp, hum, aqi):

    new_data = pd.DataFrame([{
        "timestamp": datetime.now(),
        "pm2_5": pm25,
        "pm10": pm10,
        "co": co,
        "no2": no2,
        "o3": o3,
        "so2": so2,
        "nh3": nh3,
        "temp": temp,
        "humidity": hum,
        "aqi": aqi
    }])

    if os.path.exists("dataset.csv"):

        try:
            old_df = pd.read_csv("dataset.csv")

            updated_df = pd.concat(
                [old_df, new_data],
                ignore_index=True
            )

        except:
            updated_df = new_data

    else:
        updated_df = new_data

    updated_df.to_csv(
        "dataset.csv",
        index=False
    )


weather = get_weather_data()
aqi_data = get_live_aqi()

# safety fallback (VERY IMPORTANT)
pm25 = aqi_data.get("pm25", 0)
pm10 = aqi_data.get("pm10", 0)
co = aqi_data.get("co", 0)
no2 = aqi_data.get("no2", 0)
o3 = aqi_data.get("o3", 0)
so2 = aqi_data.get("so2", 0)
nh3 = aqi_data.get("nh3", 0)

temp = weather.get("temp", 30)
hum = weather.get("humidity", 60)

st.markdown("""
### 📍 Chennai, India  
#### 🔴 Live Real-Time AQI Monitoring
""")
# ─────────────────────────────────────────────
# COMPUTE AQI
# ─────────────────────────────────────────────

aqi = predict_aqi(
    pm25,
    pm10,
    co,
    no2,
    o3,
    so2,
    nh3,
    temp,
    hum
)

label, color = get_level(aqi)

advice = get_health_advice(aqi)

# SAVE DATA
save_live_data(
    pm25,
    pm10,
    co,
    no2,
    o3,
    so2,
    nh3,
    temp,
    hum,
    aqi
)

# SEND EMAIL ALERT
if aqi >= 100:
    send_email_alert(aqi, label)

#--------------------------------------------

# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:

    st.markdown("""
    <h1 style="
    color:white;
    font-size:28px;
    font-weight:700;
    margin-bottom:0;
    ">
    🌍 PolluCast
    </h1>
    """, unsafe_allow_html=True)

    st.markdown("""
    <p style="
    color:#8E8E93;
    font-family:JetBrains Mono;
    font-size:11px;
    letter-spacing:0.1em;
    margin-bottom:30px;
    ">
    LIVE SENSOR INPUT
    </p>
    """, unsafe_allow_html=True)

    # pm25 = st.slider("PM2.5", 0.0, 500.0, 80.0)
    # pm10 = st.slider("PM10", 0.0, 500.0, 120.0)

    # temp = st.slider("Temperature", 10.0, 50.0, 30.0)

    # hum = st.slider("Humidity", 10.0, 100.0, 60.0)

    # co = st.slider("CO", 0.0, 5000.0, 800.0)

    # no2 = st.slider("NO₂", 0.0, 500.0, 40.0)

    # o3 = st.slider("O₃", 0.0, 500.0, 30.0)

    # so2 = st.slider("SO₂", 0.0, 500.0, 20.0)

    # nh3 = st.slider("NH₃", 0.0, 500.0, 10.0)
    # LIVE DATA



# # ─────────────────────────────────────────────
# # COMPUTE AQI
# # ─────────────────────────────────────────────
# # 
# aqi = predict_aqi(pm25, pm10, co, no2, o3, so2, nh3, temp, hum)

# label, color = get_level(aqi)

# # ─────────────────────────────────────────────
# # HEADER
# # ─────────────────────────────────────────────
# left, right = st.columns([4,1])

# with left:

#     st.markdown(f"""
#     <h1 style="
#     font-size:42px;
#     font-weight:700;
#     color:white;
#     margin-bottom:5px;
#     ">
#     PolluCast
#     <span style="color:#666;">Live Dashboard</span>
#     </h1>

#     <p style="
#     color:#8E8E93;
#     font-family:JetBrains Mono;
#     letter-spacing:0.08em;
#     ">
#     AI-POWERED AIR QUALITY MONITORING
#     </p>

#     <div style="
#     height:1px;
#     background:linear-gradient(
#     90deg,
#     transparent,
#     rgba(0,255,163,0.5),
#     transparent
#     );
#     margin-top:20px;
#     margin-bottom:20px;
#     ">
#     </div>
#     """, unsafe_allow_html=True)

# with right:

#     st.markdown(f"""
#     <div style="text-align:right;">

#     <div style="
#     color:#8E8E93;
#     font-size:11px;
#     font-family:JetBrains Mono;
#     letter-spacing:0.1em;
#     ">
#     AQI
#     </div>

#     <div style="
#     font-size:60px;
#     font-weight:700;
#     color:{color};
#     text-shadow:
#         0 0 12px {color},
#         0 0 25px rgba(0,255,163,0.25);
#     ">
#     {aqi}
#     </div>

#     <div style="
#     color:{color};
#     font-family:JetBrains Mono;
#     letter-spacing:0.1em;
#     ">
#     {label.upper()}
#     </div>

#     </div>
#     """, unsafe_allow_html=True)
# ─────────────────────────────────────────────
# COMPUTE AQI
# ─────────────────────────────────────────────

# aqi = predict_aqi(
#     pm25,
#     pm10,
#     co,
#     no2,
#     o3,
#     so2,
#     nh3,
#     temp,
#     hum
# )

# label, color = get_level(aqi)

# advice = get_health_advice(aqi)

# save_live_data(
#     pm25,
#     pm10,
#     co,
#     no2,
#     o3,
#     so2,
#     nh3,
#     temp,
#     hum,
#     aqi
# )
# ─────────────────────────────────────────────
# METRICS
# ─────────────────────────────────────────────
m1, m2, m3, m4 = st.columns(4)

with m1:
    st.metric("AQI", aqi)

with m2:
    st.metric("Temperature", f"{temp} °C")

with m3:
    st.metric("Humidity", f"{hum}%")

with m4:
    st.metric("PM2.5", f"{pm25}")


    st.markdown("## 🩺 Health Recommendation")

    st.markdown(f"""
<div style="
background: rgba(18,18,18,0.75);
border-left: 6px solid {color};
padding: 20px;
border-radius: 18px;
font-size: 18px;
color: white;
">
{advice}
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# AQI TREND
# ─────────────────────────────────────────────
st.markdown("## 📈 AQI Trend")

hours = list(range(24))

np.random.seed(42)

trend = [
    int(np.clip(
        aqi * (0.7 + 0.5 * np.sin(h/3))
        + np.random.randn() * 10,
        0,
        500
    ))
    for h in hours
]

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=hours,
    y=trend,
    mode="lines",
    line=dict(
        color="#00FFA3",
        width=4,
        shape="spline"
    ),
    fill="tozeroy",
    fillcolor="rgba(0,255,163,0.08)"
))

fig.update_layout(
    height=350,

    paper_bgcolor="#0D0D0D",
    plot_bgcolor="#0D0D0D",

    margin=dict(l=0, r=0, t=20, b=0),

    font=dict(
        color="white"
    ),

    xaxis=dict(
        showgrid=False,
        linecolor="rgba(255,255,255,0.08)"
    ),

    yaxis=dict(
        showgrid=True,
        gridcolor="rgba(255,255,255,0.06)",
        linecolor="rgba(255,255,255,0.08)"
    )
)

st.plotly_chart(
    fig,
    width='stretch',
    config={"displayModeBar": False}
)

# ─────────────────────────────────────────────
# POLLUTANT CARDS
# ─────────────────────────────────────────────
st.markdown("## ☁ Pollutant Levels")

pollutants = [
    ("PM2.5", pm25),
    ("PM10", pm10),
    ("CO", co),
    ("NO₂", no2),
    ("O₃", o3),
    ("SO₂", so2),
    ("NH₃", nh3)
]

cols = st.columns(7)

for col, (name, value) in zip(cols, pollutants):

    with col:

        st.markdown(f"""
        <div style="
        background:rgba(18,18,18,0.75);
        border:1px solid rgba(255,255,255,0.06);
        border-radius:18px;
        padding:18px;
        text-align:center;
        ">

        <div style="
        color:#8E8E93;
        font-size:11px;
        font-family:JetBrains Mono;
        letter-spacing:0.1em;
        ">
        {name}
        </div>

        <div style="
        color:white;
        font-size:28px;
        font-weight:700;
        margin-top:10px;
        ">
        {int(value)}
        </div>

        </div>
        """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# DATASET
# ─────────────────────────────────────────────
try:

    df = pd.read_csv("dataset.csv")

    st.markdown("## 📋 Dataset Preview")

    st.dataframe(
        df.head(10),
        width='stretch',
        hide_index=True
    )

    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="⬇ Download Dataset",
        data=csv,
        file_name="pollucast_dataset.csv",
        mime="text/csv"
    )

except:
    st.warning("dataset.csv not found")

# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown(f"""
<div style="
margin-top:50px;
padding-top:20px;
padding-bottom:20px;
border-top:1px solid rgba(255,255,255,0.06);
display:flex;
justify-content:space-between;
">

<div style="
color:#777;
font-family:JetBrains Mono;
font-size:11px;
letter-spacing:0.1em;
">
POLLUCAST • DEVELOPED BY NEHA
</div>

<div style="
color:{color};
font-weight:600;
">
AQI {aqi} • {label}
</div>

</div>
""", unsafe_allow_html=True)
try:
    weather = get_weather_data()
    aqi_data = get_live_aqi()
except:
    st.error("API failed. Using fallback values")
    weather = {"temp": 30, "humidity": 60}
    aqi_data = {"pm25": 50, "pm10": 80, "co": 0, "no2": 10, "o3": 20, "so2": 5, "nh3": 5}