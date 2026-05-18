# # # import os
# # # from datetime import datetime
# # # import streamlit as st
# # # import pandas as pd
# # # import numpy as np
# # # import plotly.graph_objects as go
# # # import joblib
# # # from utils.api import get_weather_data, get_live_aqi
# # # from streamlit_autorefresh import st_autorefresh
# # # from utils.email_alert import send_email_alert
# # # # LOAD TRAINED MODEL
# # # model = joblib.load("model.pkl")

# # # # ─────────────────────────────────────────────
# # # # PAGE CONFIG
# # # # ─────────────────────────────────────────────
# # # st.set_page_config(
# # #     page_title="PolluCast • Live Dashboard",
# # #     page_icon="🌍",
# # #     layout="wide",
# # #     initial_sidebar_state="expanded"
# # # )
# # # st_autorefresh(interval=60000, key="pollucastrefresh")
# # # # ─────────────────────────────────────────────
# # # # BLACK AESTHETIC CSS
# # # # ─────────────────────────────────────────────
# # # st.markdown("""
# # # <style>

# # # @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=JetBrains+Mono:wght@300;400;500&display=swap');

# # # html, body, [class*="css"] {
# # #     font-family: 'DM Sans', sans-serif;
# # # }

# # # .stApp {
# # #     background:
# # #         radial-gradient(circle at top left, rgba(0,255,170,0.06), transparent 25%),
# # #         radial-gradient(circle at bottom right, rgba(0,140,255,0.05), transparent 25%),
# # #         #050505;
# # #     color: #F5F5F5;
# # # }

# # # #MainMenu,
# # # footer,
# # # header {
# # #     visibility: hidden;
# # # }

# # # /* SIDEBAR */

# # # [data-testid="stSidebar"] {
# # #     background: rgba(10,10,10,0.97) !important;
# # #     border-right: 1px solid rgba(255,255,255,0.06);
# # # }

# # # [data-testid="stSidebar"] label {
# # #     color: #8E8E93 !important;
# # #     font-family: 'JetBrains Mono', monospace !important;
# # #     font-size: 11px !important;
# # #     text-transform: uppercase;
# # #     letter-spacing: 0.08em;
# # # }

# # # /* METRICS */

# # # [data-testid="metric-container"] {
# # #     background: rgba(18,18,18,0.72) !important;
# # #     border: 1px solid rgba(255,255,255,0.06) !important;
# # #     border-radius: 22px !important;
# # #     padding: 24px !important;

# # #     backdrop-filter: blur(12px);

# # #     box-shadow:
# # #         0 8px 32px rgba(0,0,0,0.45);

# # #     transition: all 0.25s ease;
# # # }

# # # [data-testid="metric-container"]:hover {
# # #     transform: translateY(-4px);
# # #     border: 1px solid rgba(0,255,163,0.20) !important;
# # #     box-shadow:
# # #         0 0 20px rgba(0,255,163,0.08),
# # #         0 10px 35px rgba(0,0,0,0.55);
# # # }

# # # [data-testid="stMetricLabel"] p {
# # #     color: #8E8E93 !important;
# # #     font-family: 'JetBrains Mono', monospace !important;
# # #     letter-spacing: 0.12em;
# # #     text-transform: uppercase;
# # #     font-size: 10px !important;
# # # }

# # # [data-testid="stMetricValue"] {
# # #     color: white !important;
# # #     font-size: 34px !important;
# # #     font-weight: 700 !important;
# # # }

# # # /* BUTTONS */

# # # .stDownloadButton > button {
# # #     background: linear-gradient(
# # #         135deg,
# # #         #00FFA3,
# # #         #00C2FF
# # #     ) !important;

# # #     color: black !important;
# # #     border: none !important;
# # #     border-radius: 14px !important;

# # #     font-weight: 600 !important;

# # #     transition: 0.25s ease;
# # # }

# # # .stDownloadButton > button:hover {
# # #     transform: scale(1.03);
# # #     box-shadow:
# # #         0 0 25px rgba(0,255,163,0.25);
# # # }

# # # /* DATAFRAME */

# # # [data-testid="stDataFrame"] {
# # #     border-radius: 20px !important;
# # #     overflow: hidden;
# # #     border: 1px solid rgba(255,255,255,0.06) !important;
# # # }

# # # /* SCROLLBAR */

# # # ::-webkit-scrollbar {
# # #     width: 6px;
# # # }

# # # ::-webkit-scrollbar-track {
# # #     background: #050505;
# # # }

# # # ::-webkit-scrollbar-thumb {
# # #     background: #222;
# # #     border-radius: 20px;
# # # }

# # # ::-webkit-scrollbar-thumb:hover {
# # #     background: #444;
# # # }

# # # </style>
# # # """, unsafe_allow_html=True)

# # # # ─────────────────────────────────────────────
# # # # AQI CALCULATION
# # # # ─────────────────────────────────────────────
# # # AQI_LEVELS = [
# # #     (50, "Good", "#00FFA3"),
# # #     (100, "Moderate", "#FFC857"),
# # #     (150, "Sensitive", "#FF7A00"),
# # #     (200, "Unhealthy", "#FF3B30"),
# # #     (300, "Very Unhealthy", "#C084FC"),
# # #     (500, "Hazardous", "#FF006E"),
# # # ]
# # # FEATURE_COLUMNS = [
# # #     "pm2_5","pm10","temp_c","humidity","co","no","no2","o3","so2","nh3",
# # #     "AQI_PM25","AQI_PM10","AQI_Category",
# # #     "hour","day","weekday","month",
# # #     "pm2_5_3h_avg","pm10_3h_avg","co_3h_avg","no_3h_avg","no2_3h_avg",
# # #     "o3_3h_avg","so2_3h_avg","nh3_3h_avg","temp_c_3h_avg","humidity_3h_avg",
# # #     "pm2_5_24h_avg","pm10_24h_avg","co_24h_avg","no_24h_avg","no2_24h_avg",
# # #     "o3_24h_avg","so2_24h_avg","nh3_24h_avg","temp_c_24h_avg","humidity_24h_avg",
# # #     "pm2_5_lag_1h","pm2_5_lag_3h","pm2_5_lag_24h",
# # #     "pm10_lag_1h","pm10_lag_3h","pm10_lag_24h",
# # #     "co_lag_1h","co_lag_3h","co_lag_24h",
# # #     "no_lag_1h","no_lag_3h","no_lag_24h",
# # #     "no2_lag_1h","no2_lag_3h","no2_lag_24h",
# # #     "o3_lag_1h","o3_lag_3h","o3_lag_24h",
# # #     "so2_lag_1h","so2_lag_3h","so2_lag_24h",
# # #     "nh3_lag_1h","nh3_lag_3h","nh3_lag_24h",
# # #     "temp_c_lag_1h","temp_c_lag_3h","temp_c_lag_24h",
# # #     "humidity_lag_1h","humidity_lag_3h","humidity_lag_24h",
# # #     "AQI_lag_1h","AQI_lag_3h","AQI_lag_24h"
# # # ]
# # # def predict_aqi(pm25, pm10, co, no2, o3, so2, nh3, temp, hum):

# # #     input_data = {
# # #         "pm2_5": pm25,
# # #         "pm10": pm10,
# # #         "temp_c": temp,
# # #         "humidity": hum,
# # #         "co": co,
# # #         "no": 0,
# # #         "no2": no2,
# # #         "o3": o3,
# # #         "so2": so2,
# # #         "nh3": nh3,

# # #         "AQI_PM25": pm25,
# # #         "AQI_PM10": pm10,
# # #         "AQI_Category": 1,

# # #         "hour": 12,
# # #         "day": 1,
# # #         "weekday": 1,
# # #         "month": 1,

# # #         "pm2_5_3h_avg": pm25,
# # #         "pm10_3h_avg": pm10,
# # #         "co_3h_avg": co,
# # #         "no_3h_avg": 0,
# # #         "no2_3h_avg": no2,
# # #         "o3_3h_avg": o3,
# # #         "so2_3h_avg": so2,
# # #         "nh3_3h_avg": nh3,
# # #         "temp_c_3h_avg": temp,
# # #         "humidity_3h_avg": hum,

# # #         "pm2_5_24h_avg": pm25,
# # #         "pm10_24h_avg": pm10,
# # #         "co_24h_avg": co,
# # #         "no_24h_avg": 0,
# # #         "no2_24h_avg": no2,
# # #         "o3_24h_avg": o3,
# # #         "so2_24h_avg": so2,
# # #         "nh3_24h_avg": nh3,
# # #         "temp_c_24h_avg": temp,
# # #         "humidity_24h_avg": hum,

# # #         "pm2_5_lag_1h": pm25,
# # #         "pm2_5_lag_3h": pm25,
# # #         "pm2_5_lag_24h": pm25,

# # #         "pm10_lag_1h": pm10,
# # #         "pm10_lag_3h": pm10,
# # #         "pm10_lag_24h": pm10,

# # #         "co_lag_1h": co,
# # #         "co_lag_3h": co,
# # #         "co_lag_24h": co,

# # #         "no_lag_1h": 0,
# # #         "no_lag_3h": 0,
# # #         "no_lag_24h": 0,

# # #         "no2_lag_1h": no2,
# # #         "no2_lag_3h": no2,
# # #         "no2_lag_24h": no2,

# # #         "o3_lag_1h": o3,
# # #         "o3_lag_3h": o3,
# # #         "o3_lag_24h": o3,

# # #         "so2_lag_1h": so2,
# # #         "so2_lag_3h": so2,
# # #         "so2_lag_24h": so2,

# # #         "nh3_lag_1h": nh3,
# # #         "nh3_lag_3h": nh3,
# # #         "nh3_lag_24h": nh3,

# # #         "temp_c_lag_1h": temp,
# # #         "temp_c_lag_3h": temp,
# # #         "temp_c_lag_24h": temp,

# # #         "humidity_lag_1h": hum,
# # #         "humidity_lag_3h": hum,
# # #         "humidity_lag_24h": hum,

# # #         "AQI_lag_1h": 100,
# # #         "AQI_lag_3h": 100,
# # #         "AQI_lag_24h": 100,
# # #     }

# # #     df = pd.DataFrame([input_data])

# # #     # FORCE SAME ORDER
# # #     df = df[FEATURE_COLUMNS]

# # #     prediction = model.predict(df)[0]

# # #     return int(round(prediction))

# # # def get_level(aqi):
# # #     for limit, label, color in AQI_LEVELS:
# # #         if aqi <= limit:
# # #             return label, color
# # #     return "Hazardous", "#FF006E"
# # # def get_health_advice(aqi):

# # #     if aqi <= 50:
# # #         return "🟢 Air quality is good. Safe for outdoor activities."

# # #     elif aqi <= 100:
# # #         return "🟡 Moderate air quality. Sensitive people should take care."

# # #     elif aqi <= 150:
# # #         return "🟠 Sensitive groups should reduce outdoor exposure."

# # #     elif aqi <= 200:
# # #         return "🔴 Unhealthy air quality. Wear a mask outdoors."

# # #     elif aqi <= 300:
# # #         return "🟣 Very unhealthy conditions. Avoid outdoor activities."

# # #     else:
# # #         return "⚫ Hazardous air quality. Stay indoors and use air purification."

# # # def save_live_data(pm25, pm10, co, no2, o3, so2, nh3, temp, hum, aqi):

# # #     new_data = pd.DataFrame([{
# # #         "timestamp": datetime.now(),
# # #         "pm2_5": pm25,
# # #         "pm10": pm10,
# # #         "co": co,
# # #         "no2": no2,
# # #         "o3": o3,
# # #         "so2": so2,
# # #         "nh3": nh3,
# # #         "temp": temp,
# # #         "humidity": hum,
# # #         "aqi": aqi
# # #     }])

# # #     if os.path.exists("dataset.csv"):

# # #         try:
# # #             old_df = pd.read_csv("dataset.csv")

# # #             updated_df = pd.concat(
# # #                 [old_df, new_data],
# # #                 ignore_index=True
# # #             )

# # #         except:
# # #             updated_df = new_data

# # #     else:
# # #         updated_df = new_data

# # #     updated_df.to_csv(
# # #         "dataset.csv",
# # #         index=False
# # #     )


# # # weather = get_weather_data()
# # # aqi_data = get_live_aqi()

# # # # safety fallback (VERY IMPORTANT)
# # # pm25 = aqi_data.get("pm25", 0)
# # # pm10 = aqi_data.get("pm10", 0)
# # # co = aqi_data.get("co", 0)
# # # no2 = aqi_data.get("no2", 0)
# # # o3 = aqi_data.get("o3", 0)
# # # so2 = aqi_data.get("so2", 0)
# # # nh3 = aqi_data.get("nh3", 0)

# # # temp = weather.get("temp", 30)
# # # hum = weather.get("humidity", 60)

# # # st.markdown("""
# # # ### 📍 Chennai, India  
# # # #### 🔴 Live Real-Time AQI Monitoring
# # # """)
# # # # ─────────────────────────────────────────────
# # # # COMPUTE AQI
# # # # ─────────────────────────────────────────────

# # # aqi = predict_aqi(
# # #     pm25,
# # #     pm10,
# # #     co,
# # #     no2,
# # #     o3,
# # #     so2,
# # #     nh3,
# # #     temp,
# # #     hum
# # # )

# # # label, color = get_level(aqi)

# # # advice = get_health_advice(aqi)

# # # # SAVE DATA
# # # save_live_data(
# # #     pm25,
# # #     pm10,
# # #     co,
# # #     no2,
# # #     o3,
# # #     so2,
# # #     nh3,
# # #     temp,
# # #     hum,
# # #     aqi
# # # )

# # # # SEND EMAIL ALERT
# # # if aqi >= 100:
# # #     send_email_alert(aqi, label)

# # # #--------------------------------------------

# # # # SIDEBAR
# # # # ─────────────────────────────────────────────
# # # with st.sidebar:

# # #     st.markdown("""
# # #     <h1 style="
# # #     color:white;
# # #     font-size:28px;
# # #     font-weight:700;
# # #     margin-bottom:0;
# # #     ">
# # #     🌍 PolluCast
# # #     </h1>
# # #     """, unsafe_allow_html=True)

# # #     st.markdown("""
# # #     <p style="
# # #     color:#8E8E93;
# # #     font-family:JetBrains Mono;
# # #     font-size:11px;
# # #     letter-spacing:0.1em;
# # #     margin-bottom:30px;
# # #     ">
# # #     LIVE SENSOR INPUT
# # #     </p>
# # #     """, unsafe_allow_html=True)

# # #     # pm25 = st.slider("PM2.5", 0.0, 500.0, 80.0)
# # #     # pm10 = st.slider("PM10", 0.0, 500.0, 120.0)

# # #     # temp = st.slider("Temperature", 10.0, 50.0, 30.0)

# # #     # hum = st.slider("Humidity", 10.0, 100.0, 60.0)

# # #     # co = st.slider("CO", 0.0, 5000.0, 800.0)

# # #     # no2 = st.slider("NO₂", 0.0, 500.0, 40.0)

# # #     # o3 = st.slider("O₃", 0.0, 500.0, 30.0)

# # #     # so2 = st.slider("SO₂", 0.0, 500.0, 20.0)

# # #     # nh3 = st.slider("NH₃", 0.0, 500.0, 10.0)
# # #     # LIVE DATA



# # # # # ─────────────────────────────────────────────
# # # # # COMPUTE AQI
# # # # # ─────────────────────────────────────────────
# # # # # 
# # # # aqi = predict_aqi(pm25, pm10, co, no2, o3, so2, nh3, temp, hum)

# # # # label, color = get_level(aqi)

# # # # # ─────────────────────────────────────────────
# # # # # HEADER
# # # # # ─────────────────────────────────────────────
# # # # left, right = st.columns([4,1])

# # # # with left:

# # # #     st.markdown(f"""
# # # #     <h1 style="
# # # #     font-size:42px;
# # # #     font-weight:700;
# # # #     color:white;
# # # #     margin-bottom:5px;
# # # #     ">
# # # #     PolluCast
# # # #     <span style="color:#666;">Live Dashboard</span>
# # # #     </h1>

# # # #     <p style="
# # # #     color:#8E8E93;
# # # #     font-family:JetBrains Mono;
# # # #     letter-spacing:0.08em;
# # # #     ">
# # # #     AI-POWERED AIR QUALITY MONITORING
# # # #     </p>

# # # #     <div style="
# # # #     height:1px;
# # # #     background:linear-gradient(
# # # #     90deg,
# # # #     transparent,
# # # #     rgba(0,255,163,0.5),
# # # #     transparent
# # # #     );
# # # #     margin-top:20px;
# # # #     margin-bottom:20px;
# # # #     ">
# # # #     </div>
# # # #     """, unsafe_allow_html=True)

# # # # with right:

# # # #     st.markdown(f"""
# # # #     <div style="text-align:right;">

# # # #     <div style="
# # # #     color:#8E8E93;
# # # #     font-size:11px;
# # # #     font-family:JetBrains Mono;
# # # #     letter-spacing:0.1em;
# # # #     ">
# # # #     AQI
# # # #     </div>

# # # #     <div style="
# # # #     font-size:60px;
# # # #     font-weight:700;
# # # #     color:{color};
# # # #     text-shadow:
# # # #         0 0 12px {color},
# # # #         0 0 25px rgba(0,255,163,0.25);
# # # #     ">
# # # #     {aqi}
# # # #     </div>

# # # #     <div style="
# # # #     color:{color};
# # # #     font-family:JetBrains Mono;
# # # #     letter-spacing:0.1em;
# # # #     ">
# # # #     {label.upper()}
# # # #     </div>

# # # #     </div>
# # # #     """, unsafe_allow_html=True)
# # # # ─────────────────────────────────────────────
# # # # COMPUTE AQI
# # # # ─────────────────────────────────────────────

# # # # aqi = predict_aqi(
# # # #     pm25,
# # # #     pm10,
# # # #     co,
# # # #     no2,
# # # #     o3,
# # # #     so2,
# # # #     nh3,
# # # #     temp,
# # # #     hum
# # # # )

# # # # label, color = get_level(aqi)

# # # # advice = get_health_advice(aqi)

# # # # save_live_data(
# # # #     pm25,
# # # #     pm10,
# # # #     co,
# # # #     no2,
# # # #     o3,
# # # #     so2,
# # # #     nh3,
# # # #     temp,
# # # #     hum,
# # # #     aqi
# # # # )
# # # # ─────────────────────────────────────────────
# # # # METRICS
# # # # ─────────────────────────────────────────────
# # # m1, m2, m3, m4 = st.columns(4)

# # # with m1:
# # #     st.metric("AQI", aqi)

# # # with m2:
# # #     st.metric("Temperature", f"{temp} °C")

# # # with m3:
# # #     st.metric("Humidity", f"{hum}%")

# # # with m4:
# # #     st.metric("PM2.5", f"{pm25}")


# # #     st.markdown("## 🩺 Health Recommendation")

# # #     st.markdown(f"""
# # # <div style="
# # # background: rgba(18,18,18,0.75);
# # # border-left: 6px solid {color};
# # # padding: 20px;
# # # border-radius: 18px;
# # # font-size: 18px;
# # # color: white;
# # # ">
# # # {advice}
# # # </div>
# # # """, unsafe_allow_html=True)

# # # # ─────────────────────────────────────────────
# # # # AQI TREND
# # # # ─────────────────────────────────────────────
# # # st.markdown("## 📈 AQI Trend")

# # # hours = list(range(24))

# # # np.random.seed(42)

# # # trend = [
# # #     int(np.clip(
# # #         aqi * (0.7 + 0.5 * np.sin(h/3))
# # #         + np.random.randn() * 10,
# # #         0,
# # #         500
# # #     ))
# # #     for h in hours
# # # ]

# # # fig = go.Figure()

# # # fig.add_trace(go.Scatter(
# # #     x=hours,
# # #     y=trend,
# # #     mode="lines",
# # #     line=dict(
# # #         color="#00FFA3",
# # #         width=4,
# # #         shape="spline"
# # #     ),
# # #     fill="tozeroy",
# # #     fillcolor="rgba(0,255,163,0.08)"
# # # ))

# # # fig.update_layout(
# # #     height=350,

# # #     paper_bgcolor="#0D0D0D",
# # #     plot_bgcolor="#0D0D0D",

# # #     margin=dict(l=0, r=0, t=20, b=0),

# # #     font=dict(
# # #         color="white"
# # #     ),

# # #     xaxis=dict(
# # #         showgrid=False,
# # #         linecolor="rgba(255,255,255,0.08)"
# # #     ),

# # #     yaxis=dict(
# # #         showgrid=True,
# # #         gridcolor="rgba(255,255,255,0.06)",
# # #         linecolor="rgba(255,255,255,0.08)"
# # #     )
# # # )

# # # st.plotly_chart(
# # #     fig,
# # #     width='stretch',
# # #     config={"displayModeBar": False}
# # # )

# # # # ─────────────────────────────────────────────
# # # # POLLUTANT CARDS
# # # # ─────────────────────────────────────────────
# # # st.markdown("## ☁ Pollutant Levels")

# # # pollutants = [
# # #     ("PM2.5", pm25),
# # #     ("PM10", pm10),
# # #     ("CO", co),
# # #     ("NO₂", no2),
# # #     ("O₃", o3),
# # #     ("SO₂", so2),
# # #     ("NH₃", nh3)
# # # ]

# # # cols = st.columns(7)

# # # for col, (name, value) in zip(cols, pollutants):

# # #     with col:

# # #         st.markdown(f"""
# # #         <div style="
# # #         background:rgba(18,18,18,0.75);
# # #         border:1px solid rgba(255,255,255,0.06);
# # #         border-radius:18px;
# # #         padding:18px;
# # #         text-align:center;
# # #         ">

# # #         <div style="
# # #         color:#8E8E93;
# # #         font-size:11px;
# # #         font-family:JetBrains Mono;
# # #         letter-spacing:0.1em;
# # #         ">
# # #         {name}
# # #         </div>

# # #         <div style="
# # #         color:white;
# # #         font-size:28px;
# # #         font-weight:700;
# # #         margin-top:10px;
# # #         ">
# # #         {int(value)}
# # #         </div>

# # #         </div>
# # #         """, unsafe_allow_html=True)

# # # # ─────────────────────────────────────────────
# # # # DATASET
# # # # ─────────────────────────────────────────────
# # # try:

# # #     df = pd.read_csv("dataset.csv")

# # #     st.markdown("## 📋 Dataset Preview")

# # #     st.dataframe(
# # #         df.head(10),
# # #         width='stretch',
# # #         hide_index=True
# # #     )

# # #     csv = df.to_csv(index=False).encode("utf-8")

# # #     st.download_button(
# # #         label="⬇ Download Dataset",
# # #         data=csv,
# # #         file_name="pollucast_dataset.csv",
# # #         mime="text/csv"
# # #     )

# # # except:
# # #     st.warning("dataset.csv not found")

# # # # ─────────────────────────────────────────────
# # # # FOOTER
# # # # ─────────────────────────────────────────────
# # # st.markdown(f"""
# # # <div style="
# # # margin-top:50px;
# # # padding-top:20px;
# # # padding-bottom:20px;
# # # border-top:1px solid rgba(255,255,255,0.06);
# # # display:flex;
# # # justify-content:space-between;
# # # ">

# # # <div style="
# # # color:#777;
# # # font-family:JetBrains Mono;
# # # font-size:11px;
# # # letter-spacing:0.1em;
# # # ">
# # # POLLUCAST • DEVELOPED BY NEHA
# # # </div>

# # # <div style="
# # # color:{color};
# # # font-weight:600;
# # # ">
# # # AQI {aqi} • {label}
# # # </div>

# # # </div>
# # # """, unsafe_allow_html=True)
# # # try:
# # #     weather = get_weather_data()
# # #     aqi_data = get_live_aqi()
# # # except:
# # #     st.error("API failed. Using fallback values")
# # #     weather = {"temp": 30, "humidity": 60}
# # #     aqi_data = {"pm25": 50, "pm10": 80, "co": 0, "no2": 10, "o3": 20, "so2": 5, "nh3": 5}

# # import os
# # from datetime import datetime

# # import joblib
# # import numpy as np
# # import pandas as pd
# # import plotly.graph_objects as go
# # import streamlit as st
# # from streamlit_autorefresh import st_autorefresh

# # from utils.api import get_live_aqi, get_weather_data
# # from utils.email_alert import send_email_alert

# # # ─────────────────────────────────────────────
# # #  PAGE CONFIG
# # # ─────────────────────────────────────────────
# # st.set_page_config(
# #     page_title="PolluCast · Live",
# #     page_icon="🌍",
# #     layout="wide",
# #     initial_sidebar_state="expanded",
# # )

# # # Auto-refresh every 60 s
# # st_autorefresh(interval=60_000, key="pollucast_refresh")

# # # ─────────────────────────────────────────────
# # #  GLOBAL CSS
# # # ─────────────────────────────────────────────
# # st.markdown("""
# # <style>
# # @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@300;400;500&display=swap');

# # html, body, [class*="css"] {
# #     font-family: 'DM Sans', sans-serif;
# #     letter-spacing: -0.01em;
# # }

# # .stApp {
# #     background-color: #F5F4F0;
# # }


# # #MainMenu, footer, header { visibility: hidden; }

# # /* ── Sidebar ── */
# # [data-testid="stSidebar"] {
# #     background: #FFFFFF !important;
# #     border-right: 1px solid #E5E3DC !important;
# # }
# # [data-testid="stSidebar"] > div:first-child {
# #     padding-top: 2rem;
# #     padding-left: 1.25rem;
# #     padding-right: 1.25rem;
# # }
# # [data-testid="stSidebar"] label {
# #     font-family: 'DM Mono', monospace !important;
# #     font-size: 11px !important;
# #     color: #8A8880 !important;
# #     letter-spacing: 0.06em !important;
# #     text-transform: uppercase !important;
# # }
# # [data-testid="stSidebar"] hr {
# #     border-color: #EDEBE4 !important;
# #     margin: 1.2rem 0 !important;
# # }

# # /* ── Metric cards ── */
# # [data-testid="metric-container"] {
# #     background: #FFFFFF !important;
# #     border: 1px solid #E5E3DC !important;
# #     border-radius: 16px !important;
# #     padding: 22px 24px !important;
# # }
# # [data-testid="metric-container"] [data-testid="stMetricLabel"] p {
# #     font-family: 'DM Mono', monospace !important;
# #     font-size: 10px !important;
# #     letter-spacing: 0.1em !important;
# #     text-transform: uppercase !important;
# #     color: #A8A49C !important;
# # }
# # [data-testid="metric-container"] [data-testid="stMetricValue"] {
# #     font-family: 'DM Sans', sans-serif !important;
# #     font-size: 30px !important;
# #     font-weight: 600 !important;
# #     color: #1A1916 !important;
# #     letter-spacing: -0.03em !important;
# # }

# # /* ── Download button ── */
# # .stDownloadButton > button {
# #     font-family: 'DM Sans', sans-serif !important;
# #     font-size: 13px !important;
# #     font-weight: 500 !important;
# #     background: #1A1916 !important;
# #     color: #F5F4F0 !important;
# #     border: none !important;
# #     border-radius: 10px !important;
# #     padding: 10px 24px !important;
# # }
# # .stDownloadButton > button:hover {
# #     background: #333028 !important;
# # }

# # /* ── Dataframe ── */
# # [data-testid="stDataFrame"] {
# #     border: 1px solid #E5E3DC !important;
# #     border-radius: 12px !important;
# # }

# # /* ── Scrollbar ── */
# # ::-webkit-scrollbar { width: 4px; height: 4px; }
# # ::-webkit-scrollbar-track { background: #F5F4F0; }
# # ::-webkit-scrollbar-thumb { background: #CFCDC6; border-radius: 4px; }
# # </style>
# # """, unsafe_allow_html=True)

# # st.markdown(f"""
# # <div style="
# # display:flex;
# # justify-content:space-between;
# # align-items:center;
# # padding:10px 16px;
# # background:#FFFFFF;
# # border:1px solid #E5E3DC;
# # border-radius:12px;
# # margin-bottom:18px;
# # ">

# # <div style="font-family:'DM Mono',monospace;font-size:10px;color:#A8A49C;">
# # 🟢 SYSTEM ONLINE · LIVE SENSOR STREAM
# # </div>

# # <div style="font-family:'DM Mono',monospace;font-size:10px;color:#A8A49C;">
# # LAST UPDATED · {datetime.now().strftime('%H:%M:%S')}
# # </div>

# # <div style="font-family:'DM Mono',monospace;font-size:10px;color:#A8A49C;">
# # REFRESH · 60s AUTO
# # </div>

# # </div>
# # """, unsafe_allow_html=True)

# # st.markdown("""
# # <div style="
# # font-family:'DM Mono',monospace;
# # font-size:10px;
# # color:#A8A49C;
# # letter-spacing:0.12em;
# # margin-bottom:10px;
# # ">
# # 🔬 AI MODEL · RANDOM FOREST · REAL-TIME PREDICTION ENGINE
# # </div>
# # """, unsafe_allow_html=True)
# # # ─────────────────────────────────────────────
# # #  CONSTANTS & HELPERS
# # # ─────────────────────────────────────────────
# # AQI_LEVELS = [
# #     (50,  "Good",               "#16A37F", "rgba(22,163,127,0.10)",  "rgba(22,163,127,0.22)",
# #      "Air quality is satisfactory. All outdoor activities are safe."),
# #     (100, "Moderate",           "#D4820A", "rgba(212,130,10,0.10)",  "rgba(212,130,10,0.22)",
# #      "Acceptable. Unusually sensitive people should limit prolonged outdoor exertion."),
# #     (150, "Unhealthy for Some", "#C45C2A", "rgba(196,92,42,0.10)",   "rgba(196,92,42,0.22)",
# #      "Sensitive groups may experience health effects."),
# #     (200, "Unhealthy",          "#C0392B", "rgba(192,57,43,0.10)",   "rgba(192,57,43,0.22)",
# #      "Everyone may begin to experience effects. Limit outdoor physical activity."),
# #     (300, "Very Unhealthy",     "#7B3FA0", "rgba(123,63,160,0.10)",  "rgba(123,63,160,0.22)",
# #      "Health alert — avoid all outdoor physical activity. Stay indoors."),
# #     (500, "Hazardous",          "#8B0000", "rgba(139,0,0,0.10)",     "rgba(139,0,0,0.22)",
# #      "Emergency conditions. Everyone must avoid any outdoor exposure immediately."),
# # ]

# # FEATURE_COLUMNS = [
# #     "pm2_5", "pm10", "temp_c", "humidity", "co", "no", "no2", "o3", "so2", "nh3",
# #     "AQI_PM25", "AQI_PM10", "AQI_Category",
# #     "hour", "day", "weekday", "month",
# #     "pm2_5_3h_avg", "pm10_3h_avg", "co_3h_avg", "no_3h_avg", "no2_3h_avg",
# #     "o3_3h_avg", "so2_3h_avg", "nh3_3h_avg", "temp_c_3h_avg", "humidity_3h_avg",
# #     "pm2_5_24h_avg", "pm10_24h_avg", "co_24h_avg", "no_24h_avg", "no2_24h_avg",
# #     "o3_24h_avg", "so2_24h_avg", "nh3_24h_avg", "temp_c_24h_avg", "humidity_24h_avg",
# #     "pm2_5_lag_1h", "pm2_5_lag_3h", "pm2_5_lag_24h",
# #     "pm10_lag_1h", "pm10_lag_3h", "pm10_lag_24h",
# #     "co_lag_1h", "co_lag_3h", "co_lag_24h",
# #     "no_lag_1h", "no_lag_3h", "no_lag_24h",
# #     "no2_lag_1h", "no2_lag_3h", "no2_lag_24h",
# #     "o3_lag_1h", "o3_lag_3h", "o3_lag_24h",
# #     "so2_lag_1h", "so2_lag_3h", "so2_lag_24h",
# #     "nh3_lag_1h", "nh3_lag_3h", "nh3_lag_24h",
# #     "temp_c_lag_1h", "temp_c_lag_3h", "temp_c_lag_24h",
# #     "humidity_lag_1h", "humidity_lag_3h", "humidity_lag_24h",
# #     "AQI_lag_1h", "AQI_lag_3h", "AQI_lag_24h",
# # ]


# # def get_level(aqi: int):
# #     for row in AQI_LEVELS:
# #         if aqi <= row[0]:
# #             return row[1:]   # label, fg, bg_rgba, border_rgba, msg
# #     return AQI_LEVELS[-1][1:]


# # def predict_aqi(model, pm25, pm10, co, no2, o3, so2, nh3, temp, hum) -> int:
# #     row = {
# #         "pm2_5": pm25, "pm10": pm10, "temp_c": temp, "humidity": hum,
# #         "co": co, "no": 0, "no2": no2, "o3": o3, "so2": so2, "nh3": nh3,
# #         "AQI_PM25": pm25, "AQI_PM10": pm10, "AQI_Category": 1,
# #         "hour": datetime.now().hour, "day": datetime.now().day,
# #         "weekday": datetime.now().weekday(), "month": datetime.now().month,
# #     }
# #     for base, val in [("pm2_5", pm25), ("pm10", pm10), ("co", co), ("no", 0),
# #                       ("no2", no2), ("o3", o3), ("so2", so2), ("nh3", nh3),
# #                       ("temp_c", temp), ("humidity", hum)]:
# #         for suf in ("3h_avg", "24h_avg"):
# #             row[f"{base}_{suf}"] = val
# #         if base not in ("temp_c", "humidity"):
# #             for lag in ("1h", "3h", "24h"):
# #                 row[f"{base}_lag_{lag}"] = val
# #     for lag in ("1h", "3h", "24h"):
# #         row[f"temp_c_lag_{lag}"] = temp
# #         row[f"humidity_lag_{lag}"] = hum
# #         row[f"AQI_lag_{lag}"] = 100
# #     df = pd.DataFrame([row]).reindex(columns=FEATURE_COLUMNS, fill_value=0)
# #     missing = set(FEATURE_COLUMNS) - set(df.columns)
# #     if missing:
# #         raise ValueError(f"Missing features: {missing}")
# #     return int(round(model.predict(df)[0]))


# # def save_live_data(pm25, pm10, co, no2, o3, so2, nh3, temp, hum, aqi):
# #     new_row = pd.DataFrame([{
# #         "timestamp": datetime.now().isoformat(),
# #         "pm2_5": pm25, "pm10": pm10, "co": co, "no2": no2,
# #         "o3": o3, "so2": so2, "nh3": nh3,
# #         "temp": temp, "humidity": hum, "aqi": aqi,
# #     }])
# #     path = "dataset.csv"
# #     try:
# #         base = pd.read_csv(path) if os.path.exists(path) else pd.DataFrame()
# #         pd.concat([base, new_row], ignore_index=True).to_csv(path, index=False)
# #     except Exception:
# #         new_row.to_csv(path, index=False)


# # def apply_chart_theme(fig, height=260):
# #     fig.update_layout(
# #         height=height,
# #         margin=dict(l=0, r=0, t=12, b=0),
# #         paper_bgcolor="rgba(0,0,0,0)",
# #         plot_bgcolor="rgba(0,0,0,0)",
# #         font=dict(family="DM Mono, monospace", size=10, color="#A8A49C"),
# #         hoverlabel=dict(
# #             bgcolor="#FFFFFF", bordercolor="#E5E3DC",
# #             font=dict(family="DM Sans, sans-serif", size=12, color="#1A1916"),
# #         ),
# #     )
# #     fig.update_xaxes(
# #         showgrid=False, linecolor="#E5E3DC",
# #         tickfont=dict(family="DM Mono, monospace", size=9, color="#A8A49C"),
# #     )
# #     fig.update_yaxes(
# #         showgrid=True, gridcolor="#EDEBE4", linecolor="#E5E3DC",
# #         tickfont=dict(family="DM Mono, monospace", size=9, color="#A8A49C"),
# #     )
# #     return fig


# # def section_label(text: str):
# #     st.markdown(
# #         f'<p style="font-family:\'DM Mono\',monospace; font-size:10px; '
# #         f'text-transform:uppercase; letter-spacing:0.12em; '
# #         f'color:#A8A49C; margin:28px 0 12px 2px;">{text}</p>',
# #         unsafe_allow_html=True,
# #     )


# # # ─────────────────────────────────────────────
# # #  LOAD MODEL
# # # ─────────────────────────────────────────────
# # @st.cache_resource
# # def load_model():
# #     return joblib.load("model.pkl")

# # try:
# #     model = load_model()
# # except:
# #     st.error("Model not found!")
# #     st.stop()

# # # ─────────────────────────────────────────────
# # #  FETCH LIVE DATA  (with graceful fallback)
# # # ─────────────────────────────────────────────
# # try:
# #     weather  = get_weather_data()
# #     aqi_data = get_live_aqi()
# # except Exception:
# #     weather  = {}
# #     aqi_data = {}
# # def safe_float(v, default):
# #     try:
# #         return float(v)
# #     except:
# #         return default
# # pm25 = float(aqi_data.get("pm25", 50))
# # pm10 = float(aqi_data.get("pm10", 80))
# # co   = float(aqi_data.get("co",   400))
# # no2  = float(aqi_data.get("no2",  20))
# # o3   = float(aqi_data.get("o3",   25))
# # so2  = float(aqi_data.get("so2",  10))
# # nh3  = float(aqi_data.get("nh3",  5))
# # temp = float(weather.get("temp",  30))
# # hum  = float(weather.get("humidity", 60))

# # # ─────────────────────────────────────────────
# # #  COMPUTE
# # # ─────────────────────────────────────────────
# # aqi = predict_aqi(model, pm25, pm10, co, no2, o3, so2, nh3, temp, hum)
# # label, fg, bg_rgba, border_rgba, msg = get_level(aqi)
# # hours = list(range(24))
# # np.random.seed(int(aqi))   # seed varies with AQI so chart shifts meaningfully

# # save_live_data(pm25, pm10, co, no2, o3, so2, nh3, temp, hum, aqi)

# # if "last_alert" not in st.session_state:
# #     st.session_state.last_alert = datetime.min

# # if aqi >= 100:
# #     if (datetime.now() - st.session_state.last_alert).total_seconds() > 1800:  # 30 min cooldown
# #         send_email_alert(aqi, label)
# #         st.session_state.last_alert = datetime.now()
# # # ─────────────────────────────────────────────
# # #  SIDEBAR
# # # ─────────────────────────────────────────────
# # # ─────────────────────────────
# # # DARK MODE TOGGLE
# # # ─────────────────────────────
# # theme = st.toggle("🌗 Dark Mode", value=False)

# # if theme:
# #     BG = "#0E0F12"
# #     CARD = "#16181D"
# #     TEXT = "#F5F5F5"
# #     MUTED = "#A8A8A8"
# #     BORDER = "#2A2D35"
# # else:
# #     BG = "#F5F4F0"
# #     CARD = "#FFFFFF"
# #     TEXT = "#1A1916"
# #     MUTED = "#A8A49C"
# #     BORDER = "#E5E3DC"
# # with st.sidebar:
    
# #     st.markdown("""
# #     <div style="margin-bottom:24px;">
# #       <div style="font-family:'DM Sans',sans-serif; font-size:18px;
# #                   font-weight:600; color:#1A1916; letter-spacing:-0.03em;">
# #         PolluCast
# #       </div>
# #       <div style="font-family:'DM Mono',monospace; font-size:10px;
# #                   color:#B8B5AD; letter-spacing:0.08em; margin-top:3px;">
# #         LIVE SENSOR FEED
# #       </div>
# #     </div>
# #     """, unsafe_allow_html=True)

# #     st.markdown(f"""
# #     <div style="background:#F5F4F0; border-radius:12px; padding:14px 16px; margin-bottom:20px;">
# #       <div style="font-family:'DM Mono',monospace; font-size:9px; color:#A8A49C;
# #                   letter-spacing:0.1em; margin-bottom:6px;">LOCATION</div>
# #       <div style="font-family:'DM Sans',sans-serif; font-size:14px; font-weight:500;
# #                   color:#1A1916;">Chennai, India</div>
# #       <div style="font-family:'DM Mono',monospace; font-size:10px; color:#A8A49C;
# #                   margin-top:2px;">{datetime.now().strftime('%d %b %Y · %H:%M')}</div>
# #     </div>
# #     """, unsafe_allow_html=True)

# #     st.divider()

# #     for lbl, val, unit in [
# #         ("PM2.5", pm25, "µg/m³"), ("PM10", pm10, "µg/m³"),
# #         ("CO",    co,   "µg/m³"), ("NO₂",  no2,  "µg/m³"),
# #         ("O₃",    o3,   "µg/m³"), ("SO₂",  so2,  "µg/m³"),
# #         ("NH₃",   nh3,  "µg/m³"), ("Temp", temp, "°C"),
# #         ("Humidity", hum, "%"),
# #     ]:
# #         st.markdown(
# #             f'<div style="display:flex; justify-content:space-between; '
# #             f'padding:5px 0; border-bottom:1px solid #F0EEE8;">'
# #             f'<span style="font-family:DM Mono,monospace; font-size:10px; color:#A8A49C;">{lbl}</span>'
# #             f'<span style="font-family:DM Sans,sans-serif; font-size:12px; font-weight:500; '
# #             f'color:#1A1916;">{val:.1f} {unit}</span></div>',
# #             unsafe_allow_html=True,
# #         )

# #     st.markdown("""
# #     <div style="margin-top:28px; padding-top:14px; border-top:1px solid #EDEBE4;
# #                 font-family:'DM Mono',monospace; font-size:9px;
# #                 color:#C8C5BC; letter-spacing:0.08em; line-height:2.2;">
# #       POLLUCAST v2.0 · PG PROJECT 2026<br>DEVELOPED BY NEHA
# #     </div>
# #     """, unsafe_allow_html=True)


# # # ─────────────────────────────────────────────
# # #  HEADER
# # # ─────────────────────────────────────────────
# # head_l, head_r = st.columns([3, 1], gap="large")

# # with head_l:
# #     st.markdown(f"""
# #     <h1 style="font-family:'DM Sans',sans-serif; font-size:26px; font-weight:600;
# #                color:#1A1916; letter-spacing:-0.04em; margin:0 0 4px;">
# #       PolluCast <span style="color:#A8A49C; font-weight:300;">Live Dashboard</span>
# #     </h1>
# #     <p style="font-family:'DM Mono',monospace; font-size:10px; color:#A8A49C;
# #               letter-spacing:0.08em; margin:0;">
# #       📍 CHENNAI, INDIA &nbsp;·&nbsp; AI-POWERED AIR QUALITY MONITORING &nbsp;·&nbsp;
# #       AUTO-REFRESHES EVERY 60 s
# #     </p>
# #     """, unsafe_allow_html=True)

# # with head_r:
# #     st.markdown(f"""
# #     <div style="
# #     text-align:right;
# #     padding:10px 14px;
# #     background:#FFFFFF;
# #     border:1px solid #E5E3DC;
# #     border-radius:14px;
# #     ">

# #     <div style="font-family:'DM Mono',monospace;font-size:9px;color:#A8A49C;">
# #     LIVE AQI INDEX
# #     </div>

# #     <div style="
# #     font-family:'DM Sans',sans-serif;
# #     font-size:52px;
# #     font-weight:600;
# #     color:{fg};
# #     line-height:1;
# #     margin-top:4px;
# #     ">
# #     {aqi}
# #     </div>

# #     <div style="
# #     font-family:'DM Mono',monospace;
# #     font-size:10px;
# #     color:{fg};
# #     letter-spacing:0.1em;
# #     ">
# #     {label.upper()}
# #     </div>

# #     </div>
# #     """, unsafe_allow_html=True)

# # st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)


# # # ─────────────────────────────────────────────
# # #  HEALTH ALERT BANNER
# # # ─────────────────────────────────────────────
# # st.markdown(f"""
# # <div style="background:{bg_rgba}; border:1px solid {border_rgba};
# #             border-left:3px solid {fg}; border-radius:14px;
# #             padding:15px 20px; display:flex; gap:16px; align-items:flex-start;
# #             margin-bottom:24px;">
# #   <div style="flex:1;">
# #     <div style="font-family:'DM Sans',sans-serif; font-size:13px;
# #                 font-weight:600; color:{fg}; margin-bottom:3px;">{label}</div>
# #     <div style="font-family:'DM Sans',sans-serif; font-size:13px;
# #                 color:#5A5850; line-height:1.55;">{msg}</div>
# #   </div>
# #   <div style="font-family:'DM Sans',sans-serif; font-size:36px; font-weight:600;
# #               color:{fg}; opacity:0.12; letter-spacing:-0.04em;
# #               flex-shrink:0; align-self:center;">{aqi:03d}</div>
# # </div>
# # """, unsafe_allow_html=True)


# # # ─────────────────────────────────────────────
# # #  METRIC ROW
# # # ─────────────────────────────────────────────
# # section_label("Live environmental metrics")
# # m1, m2, m3, m4, m5 = st.columns([1.2,1.2,1.2,1.2,1.2], gap="large")

# # with m1: st.metric("🌫  AQI Index",   str(aqi))
# # with m2: st.metric("📊  Category",    label)
# # with m3: st.metric("🌡  Temperature", f"{temp:.1f} °C")
# # with m4: st.metric("💧  Humidity",    f"{hum:.0f}%")
# # with m5: st.metric("☁  PM2.5",       f"{pm25:.0f} µg/m³")

# # def divider():
# #     st.markdown("""
# #     <div style="
# #     height:1px;
# #     background:linear-gradient(90deg, transparent, #E5E3DC, transparent);
# #     margin:20px 0;
# #     "></div>
# #     """, unsafe_allow_html=True)
# # # ─────────────────────────────────────────────
# # #  GAUGE + TREND
# # # ─────────────────────────────────────────────
# # section_label("AQI gauge & 24-hour simulation")
# # gauge_col, trend_col = st.columns([1, 2], gap="large")

# # needle_deg = -90 + (min(aqi, 500) / 500) * 180
# # tick_marks = "".join([
# #     f'<line x1="130" y1="36" x2="130" y2="28" stroke="#CFCDC6" stroke-width="1.5" '
# #     f'transform="rotate({-90 + (v / 500) * 180} 130 140)"/>'
# #     for v in [0, 50, 100, 150, 200, 300, 400, 500]
# # ])
# # legend_items = "".join([
# #     f'<span style="font-family:DM Mono,monospace;font-size:8px;'
# #     f'color:{c};letter-spacing:0.08em;">{n}</span>'
# #     for n, c in [("GOOD","#16A37F"),("MODERATE","#D4820A"),
# #                  ("SENSITIVE","#C45C2A"),("UNHEALTHY","#C0392B")]
# # ])

# # with gauge_col:
# #     st.markdown(f"""
# #     <div style="background:#FFFFFF; border:1px solid #E5E3DC; border-radius:16px;
# #                 padding:22px; display:flex; flex-direction:column; align-items:center;">
# #       <div style="font-family:'DM Mono',monospace; font-size:9px; color:#A8A49C;
# #                   letter-spacing:0.12em; text-transform:uppercase;
# #                   margin-bottom:14px; align-self:flex-start;">Real-time AQI sensor</div>
# #       <svg viewBox="0 0 260 155" width="220" height="128" role="img" aria-label="AQI gauge {aqi}">
# #         <defs>
# #           <filter id="gl"><feGaussianBlur stdDeviation="3" result="b"/>
# #             <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
# #           </filter>
# #         </defs>
# #         <path d="M 25,140 A 105,105 0 0,1 235,140" fill="none" stroke="#F0EEE8" stroke-width="18"/>
# #         <path d="M 25,140 A 105,105 0 0,1 72,55"   fill="none" stroke="#16A37F" stroke-width="18" opacity=".85"/>
# #         <path d="M 72,55 A 105,105 0 0,1 130,35"   fill="none" stroke="#D4820A" stroke-width="18" opacity=".85"/>
# #         <path d="M 130,35 A 105,105 0 0,1 188,55"  fill="none" stroke="#C45C2A" stroke-width="18" opacity=".85"/>
# #         <path d="M 188,55 A 105,105 0 0,1 235,140" fill="none" stroke="#C0392B" stroke-width="18" opacity=".85"/>
# #         {tick_marks}
# #         <line x1="130" y1="140" x2="130" y2="50" stroke="{fg}" stroke-width="5"
# #               stroke-linecap="round" opacity=".08" transform="rotate({needle_deg} 130 140)"/>
# #         <line x1="130" y1="140" x2="130" y2="54" stroke="{fg}" stroke-width="1.8"
# #               stroke-linecap="round" filter="url(#gl)" transform="rotate({needle_deg} 130 140)"/>
# #         <circle cx="130" cy="140" r="8" fill="#FFF" stroke="#E5E3DC" stroke-width="1.5"/>
# #         <circle cx="130" cy="140" r="3.5" fill="{fg}"/>
# #         <text x="130" y="112" font-size="32" font-weight="600" text-anchor="middle"
# #               fill="{fg}" font-family="DM Sans,sans-serif" letter-spacing="-1">{aqi}</text>
# #         <text x="130" y="128" font-size="9" text-anchor="middle" fill="#A8A49C"
# #               font-family="DM Mono,monospace" letter-spacing="1.5">{label.upper()}</text>
# #         <text x="14"  y="150" font-size="8" fill="#CFCDC6" font-family="DM Mono,monospace">0</text>
# #         <text x="113" y="30"  font-size="8" fill="#CFCDC6" font-family="DM Mono,monospace">250</text>
# #         <text x="222" y="150" font-size="8" fill="#CFCDC6" font-family="DM Mono,monospace">500</text>
# #       </svg>
# #       <div style="display:flex; gap:14px; margin-top:8px; flex-wrap:wrap; justify-content:center;">
# #         {legend_items}
# #       </div>
# #     </div>
# #     """, unsafe_allow_html=True)

# # with trend_col:
# #     trend = [
# #         int(np.clip(aqi * (0.72 + 0.55 * np.sin(h / 3.2)) + np.random.randn() * 14, 0, 500))
# #         for h in hours
# #     ]
# #     fig = go.Figure()
# #     fig.add_trace(go.Scatter(
# #         x=hours, y=trend, mode="lines",
# #         line=dict(color=fg, width=0), fill="tozeroy",
# #         fillcolor="rgba(22,163,127,0.07)", hoverinfo="skip", showlegend=False,
# #     ))
# #     fig.add_trace(go.Scatter(
# #         x=hours, y=trend, mode="lines",
# #         line=dict(color=fg, width=2.5, shape="spline"),
# #         hovertemplate="<b>%{x}:00</b> — AQI %{y}<extra></extra>",
# #     ))
# #     for thresh, col, lbl in [
# #         (50,"#16A37F","Good"), (100,"#D4820A","Mod"),
# #         (150,"#C45C2A","Sens"), (200,"#C0392B","Unhl"),
# #     ]:
# #         fig.add_hline(y=thresh, line_dash="dot", line_color=col, line_width=1, opacity=0.3,
# #                       annotation_text=lbl,
# #                       annotation_font=dict(color=col, size=9, family="DM Mono, monospace"),
# #                       annotation_position="right")
# #     fig = apply_chart_theme(fig, height=270)
# #     fig.update_layout(
# #         showlegend=False,
# #         yaxis=dict(title="AQI", range=[0, 540],
# #                    tickfont=dict(color="#A8A49C", family="DM Mono, monospace", size=9)),
# #         xaxis=dict(title="Hour", tickvals=list(range(0, 24, 4)),
# #                    ticktext=[f"{h:02d}:00" for h in range(0, 24, 4)],
# #                    tickfont=dict(color="#A8A49C", family="DM Mono, monospace", size=9)),
# #     )
# #     st.markdown("""
# #     <div style="background:#FFFFFF; border:1px solid #E5E3DC;
# # border-top:3px solid {fg};">
# #       <div style="font-family:'DM Mono',monospace; font-size:9px; color:#A8A49C;
# #                   letter-spacing:0.12em; text-transform:uppercase; margin-bottom:4px;">
# #         24-hour AQI simulation
# #       </div>
# #     """, unsafe_allow_html=True)
# #     st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
# #     st.markdown("</div>", unsafe_allow_html=True)


# # # ─────────────────────────────────────────────
# # #  POLLUTANT BREAKDOWN
# # # ─────────────────────────────────────────────
# # section_label("Pollutant concentration breakdown")

# # POLLS = [
# #     ("PM2.5", pm25, 500,  "#16A37F", "µg/m³"),
# #     ("PM10",  pm10, 500,  "#2E9E8A", "µg/m³"),
# #     ("CO",    co,   5000, "#D4820A", "µg/m³"),
# #     ("NO₂",   no2,  500,  "#C45C2A", "µg/m³"),
# #     ("O₃",    o3,   500,  "#7B3FA0", "µg/m³"),
# #     ("SO₂",   so2,  500,  "#C0392B", "µg/m³"),
# #     ("NH₃",   nh3,  500,  "#2980B9", "µg/m³"),
# # ]

# # poll_cols = st.columns(7)
# # for col, (name, val, mx, clr, unit) in zip(poll_cols, POLLS):
# #     # pct = min(int(val / mx * 100), 100)
# #     pct = min(int((val / mx) * 100) if mx else 0, 100)
# #     text_color = "#C0392B" if pct > 65 else "#1A1916"
# #     with col:
# #         st.markdown(f"""
# #         <div style="background:#FFFFFF; border:1px solid #E5E3DC;
# #                     border-top:3px solid {clr};
# #           <div style="font-family:'DM Mono',monospace; font-size:9px; color:#A8A49C;
# #                       text-transform:uppercase; letter-spacing:0.1em; margin-bottom:8px;">{name}</div>
# #           <div style="font-family:'DM Sans',sans-serif; font-size:22px; font-weight:600;
# #                       color:{text_color}; letter-spacing:-0.03em; line-height:1;
# #                       margin-bottom:2px;">{val:.0f}</div>
# #           <div style="font-family:'DM Mono',monospace; font-size:9px; color:#CFCDC6;
# #                       margin-bottom:10px;">{unit}</div>
# #           <div style="background:#F0EEE8; border-radius:2px; height:3px; overflow:hidden;">
# #             <div style="width:{pct}%; height:100%; background:{clr}; border-radius:2px;"></div>
# #           </div>
# #           <div style="font-family:'DM Mono',monospace; font-size:8px; color:#CFCDC6;
# #                       margin-top:5px; text-align:right;">{pct}%</div>
# #         </div>
# #         """, unsafe_allow_html=True)


# # # ─────────────────────────────────────────────
# # #  TEMP + HUMIDITY CHART
# # # ─────────────────────────────────────────────
# # section_label("Atmospheric conditions · temperature & humidity")

# # temp_vals = [round(temp * (0.9 + 0.2 * np.sin(h / 4)) + np.random.randn(), 1) for h in hours]
# # hum_vals  = [round(hum  * (0.85 + 0.3 * np.cos(h / 5)) + np.random.randn(), 1) for h in hours]

# # fig2 = go.Figure()
# # fig2.add_trace(go.Scatter(
# #     x=hours, y=temp_vals, name="Temp °C", mode="lines",
# #     line=dict(color="#C45C2A", width=2, shape="spline"),
# #     fill="tozeroy", fillcolor="rgba(196,92,42,0.05)",
# #     hovertemplate="<b>%{x}:00</b> — %{y}°C<extra></extra>",
# # ))
# # fig2.add_trace(go.Scatter(
# #     x=hours, y=hum_vals, name="Humidity %", mode="lines",
# #     line=dict(color="#2980B9", width=2, shape="spline", dash="dot"),
# #     hovertemplate="<b>%{x}:00</b> — %{y}%<extra></extra>",
# #     yaxis="y2",
# # ))
# # fig2 = apply_chart_theme(fig2, height=230)
# # fig2.update_layout(
# #     yaxis=dict(title="Temp °C", gridcolor="#EDEBE4",
# #                tickfont=dict(color="#A8A49C", family="DM Mono, monospace", size=9)),
# #     yaxis2=dict(title="Humidity %", overlaying="y", side="right", showgrid=False,
# #                 linecolor="#E5E3DC",
# #                 tickfont=dict(color="#A8A49C", family="DM Mono, monospace", size=9)),
# #     xaxis=dict(tickvals=list(range(0, 24, 4)),
# #                ticktext=[f"{h:02d}:00" for h in range(0, 24, 4)],
# #                tickfont=dict(color="#A8A49C", family="DM Mono, monospace", size=9)),
# #     showlegend=True,
# #     legend=dict(orientation="h", yanchor="bottom", y=1.04, xanchor="right", x=1,
# #                 font=dict(family="DM Sans, sans-serif", size=11, color="#5A5850"),
# #                 bgcolor="rgba(0,0,0,0)", bordercolor="rgba(0,0,0,0)"),
# # )

# # st.markdown("""
# # <div style="background:#FFFFFF; border:1px solid #E5E3DC; border-radius:16px; padding:20px 18px 6px;">
# #   <div style="font-family:'DM Mono',monospace; font-size:9px; color:#A8A49C;
# #               letter-spacing:0.12em; text-transform:uppercase; margin-bottom:4px;">
# #     Temperature & humidity · 24-hour simulation
# #   </div>
# # """, unsafe_allow_html=True)
# # st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})
# # st.markdown("</div>", unsafe_allow_html=True)


# # # ─────────────────────────────────────────────
# # #  DATASET PREVIEW
# # # ─────────────────────────────────────────────
# # try:
# #     df = pd.read_csv("dataset.csv")
# #     section_label("Recorded dataset")
# #     st.dataframe(df.tail(10), use_container_width=True, hide_index=True)
# #     csv_bytes = df.to_csv(index=False).encode("utf-8")
# #     st.download_button(
# #         label="⬇  Export full dataset  (.csv)",
# #         data=csv_bytes,
# #         file_name="pollucast_dataset.csv",
# #         mime="text/csv",
# #     )
# # except FileNotFoundError:
# #     pass


# # # ─────────────────────────────────────────────
# # #  FOOTER
# # # ─────────────────────────────────────────────
# # st.markdown(f"""
# # <div style="margin-top:48px; padding:16px 0; border-top:1px solid #E5E3DC;
# #             display:flex; justify-content:space-between; align-items:center;">
# #   <div style="font-family:'DM Mono',monospace; font-size:9px;
# #               color:#C8C5BC; letter-spacing:0.1em;">
# #     POLLUCAST LIVE · DEVELOPED BY NEHA · PG PROJECT 2026
# #   </div>
# #   <div style="font-family:'DM Sans',sans-serif; font-size:13px;
# #               font-weight:500; color:{fg};">
# #     AQI {aqi} · {label}
# #   </div>
# # </div>
# # """, unsafe_allow_html=True)

# ##3

# import os
# from datetime import datetime

# import joblib
# import numpy as np
# import pandas as pd
# import plotly.graph_objects as go
# import streamlit as st
# from streamlit_autorefresh import st_autorefresh

# from utils.api import get_live_aqi, get_weather_data
# from utils.email_alert import send_email_alert
# from utils.sms_alert import send_sms_alert

# # ─────────────────────────────────────────────
# # PAGE CONFIG
# # ─────────────────────────────────────────────
# st.set_page_config(
#     page_title="PolluCast · Live",
#     page_icon="🌍",
#     layout="wide",
#     initial_sidebar_state="expanded",
# )

# st_autorefresh(interval=60_000, key="pollucast_refresh")


# # ─────────────────────────────────────────────
# # CSS (LIGHT MODE DESIGN)
# # ─────────────────────────────────────────────
# st.markdown("""
# <style>
# html, body {
#     font-family: 'DM Sans', sans-serif;
#     background: #F5F4F0;
# }
# </style>
# """, unsafe_allow_html=True)


# # ─────────────────────────────────────────────
# # LOAD MODEL
# # ─────────────────────────────────────────────
# @st.cache_resource
# def load_model():
#     return joblib.load("model.pkl")

# model = load_model()


# # ─────────────────────────────────────────────
# # AQI LEVELS
# # ─────────────────────────────────────────────
# AQI_LEVELS = [
#     (50, "Good", "#16A37F", "Air quality is good."),
#     (100, "Moderate", "#D4820A", "Acceptable air quality."),
#     (150, "Unhealthy for Sensitive", "#C45C2A", "Sensitive groups affected."),
#     (200, "Unhealthy", "#C0392B", "Health effects possible."),
#     (300, "Very Unhealthy", "#7B3FA0", "Avoid outdoor activity."),
#     (500, "Hazardous", "#8B0000", "Emergency conditions."),
# ]


# def get_level(aqi):
#     for limit, label, color, msg in AQI_LEVELS:
#         if aqi <= limit:
#             return label, color, msg
#     return AQI_LEVELS[-1][1:]


# # ─────────────────────────────────────────────
# # SAFE FLOAT
# # ─────────────────────────────────────────────
# def safe(v, default=0.0):
#     try:
#         return float(v)
#     except:
#         return default


# # ─────────────────────────────────────────────
# # FEATURE ENGINE (FIXED + SAFE)
# # ─────────────────────────────────────────────
# FEATURE_COLUMNS = model.feature_names_in_


# def build_features(pm25, pm10, co, no2, o3, so2, nh3, temp, hum):
#     row = {col: 0 for col in FEATURE_COLUMNS}

#     now = datetime.now()

#     base = {
#         "pm2_5": pm25,
#         "pm10": pm10,
#         "co": co,
#         "no2": no2,
#         "o3": o3,
#         "so2": so2,
#         "nh3": nh3,
#         "temp_c": temp,
#         "humidity": hum,
#     }

#     for k, v in base.items():
#         if k in row:
#             row[k] = v

#     row["hour"] = now.hour
#     row["day"] = now.day
#     row["weekday"] = now.weekday()
#     row["month"] = now.month

#     return pd.DataFrame([row])[FEATURE_COLUMNS]


# # ─────────────────────────────────────────────
# # PREDICT
# # ─────────────────────────────────────────────
# def predict_aqi(pm25, pm10, co, no2, o3, so2, nh3, temp, hum):
#     df = build_features(pm25, pm10, co, no2, o3, so2, nh3, temp, hum)
#     pred = model.predict(df)[0]
#     return int(round(pred))


# # ─────────────────────────────────────────────
# # SAVE DATA
# # ─────────────────────────────────────────────
# def save_live_data(pm25, pm10, co, no2, o3, so2, nh3, temp, hum, aqi):
#     row = pd.DataFrame([{
#         "timestamp": datetime.now().isoformat(),
#         "pm2_5": pm25,
#         "pm10": pm10,
#         "co": co,
#         "no2": no2,
#         "o3": o3,
#         "so2": so2,
#         "nh3": nh3,
#         "temp": temp,
#         "humidity": hum,
#         "aqi": aqi,
#     }])

#     file = "dataset.csv"

#     if os.path.exists(file):
#         old = pd.read_csv(file)
#         pd.concat([old, row], ignore_index=True).to_csv(file, index=False)
#     else:
#         row.to_csv(file, index=False)


# # ─────────────────────────────────────────────
# # FETCH DATA (SAFE)
# # ─────────────────────────────────────────────
# try:
#     weather = get_weather_data()
#     aqi_data = get_live_aqi()
# except:
#     weather = {}
#     aqi_data = {}


# pm25 = safe(aqi_data.get("pm25", 50))
# pm10 = safe(aqi_data.get("pm10", 80))
# co   = safe(aqi_data.get("co", 400))
# no2  = safe(aqi_data.get("no2", 20))
# o3   = safe(aqi_data.get("o3", 25))
# so2  = safe(aqi_data.get("so2", 10))
# nh3  = safe(aqi_data.get("nh3", 5))

# temp = safe(weather.get("temp", 30))
# hum  = safe(weather.get("humidity", 60))


# # ─────────────────────────────────────────────
# # COMPUTE AQI
# # ─────────────────────────────────────────────
# aqi = predict_aqi(pm25, pm10, co, no2, o3, so2, nh3, temp, hum)
# label, color, msg = get_level(aqi)

# save_live_data(pm25, pm10, co, no2, o3, so2, nh3, temp, hum, aqi)


# # ─────────────────────────────────────────────
# # ALERT SYSTEM
# # ─────────────────────────────────────────────
# # if "last_alert" not in st.session_state:
# #     st.session_state.last_alert = datetime.min
# # if "sms_sent" not in st.session_state:
# #     st.session_state.sms_sent = False

# # if aqi >= 100 and not st.session_state.sms_sent:
# #     send_email_alert(aqi, label)
# #     send_sms_alert(aqi, label)
# #     st.session_state.sms_sent = True
# # if aqi >= 100:
# #     if (datetime.now() - st.session_state.last_alert).seconds > 1800:
# #         send_email_alert(aqi, label)
# #         send_sms_alert(aqi, label)
# #         st.session_state.last_alert = datetime.now()
# if "alert_sent" not in st.session_state:
#     st.session_state.alert_sent = False

# if aqi >= 100 and not st.session_state.alert_sent:
#     send_email_alert(aqi, label)
#     send_sms_alert(aqi, label)
#     st.session_state.alert_sent = True

# if aqi < 100:
#     st.session_state.alert_sent = False

# # ─────────────────────────────────────────────
# # HEADER
# # ─────────────────────────────────────────────
# st.title("🌍 PolluCast Live Dashboard")
# st.caption("AI-powered real-time air quality monitoring")


# # ─────────────────────────────────────────────
# # METRICS
# # ─────────────────────────────────────────────
# col1, col2, col3, col4 = st.columns(4)

# col1.metric("AQI", aqi)
# col2.metric("Category", label)
# col3.metric("Temperature", f"{temp:.1f} °C")
# col4.metric("Humidity", f"{hum:.0f} %")


# # ─────────────────────────────────────────────
# # HEALTH MESSAGE
# # ─────────────────────────────────────────────
# st.markdown(f"""
# ### 🩺 Health Advisory
# <div style="padding:15px;background:{color}22;border-left:5px solid {color};border-radius:10px">
# {msg}
# </div>
# """, unsafe_allow_html=True)


# # ─────────────────────────────────────────────
# # TREND CHART
# # ─────────────────────────────────────────────
# hours = list(range(24))
# trend = [max(0, min(500, aqi + np.random.randint(-30, 30))) for _ in hours]

# fig = go.Figure()
# fig.add_trace(go.Scatter(x=hours, y=trend, mode="lines", line=dict(color=color)))
# st.plotly_chart(fig, width="stretch")


# # ─────────────────────────────────────────────
# # POLLUTANTS
# # ─────────────────────────────────────────────
# st.subheader("☁ Pollutants")

# st.write({
#     "PM2.5": pm25,
#     "PM10": pm10,
#     "CO": co,
#     "NO2": no2,
#     "O3": o3,
#     "SO2": so2,
#     "NH3": nh3
# })


# # ─────────────────────────────────────────────
# # DATASET
# # ─────────────────────────────────────────────
# if os.path.exists("dataset.csv"):
#     df = pd.read_csv("dataset.csv")
#     st.subheader("📊 Dataset")
#     st.dataframe(df.tail(10))
#     st.download_button("Download CSV", df.to_csv(index=False), "dataset.csv")



##$
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
from utils.sms_alert import send_sms_alert

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
# CSS (LIGHT MODE DESIGN)
# ─────────────────────────────────────────────
st.markdown("""
<style>
html, body {
    font-family: 'DM Sans', sans-serif;
    background: #F5F4F0;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# LOAD MODEL
# ─────────────────────────────────────────────
@st.cache_resource
def load_model():
    return joblib.load("model.pkl")

model = load_model()


# ─────────────────────────────────────────────
# AQI LEVELS
# ─────────────────────────────────────────────
AQI_LEVELS = [
    (50, "Good", "#16A37F", "Air quality is good."),
    (100, "Moderate", "#D4820A", "Acceptable air quality."),
    (150, "Unhealthy for Sensitive", "#C45C2A", "Sensitive groups affected."),
    (200, "Unhealthy", "#C0392B", "Health effects possible."),
    (300, "Very Unhealthy", "#7B3FA0", "Avoid outdoor activity."),
    (500, "Hazardous", "#8B0000", "Emergency conditions."),
]


def get_level(aqi):
    for limit, label, color, msg in AQI_LEVELS:
        if aqi <= limit:
            return label, color, msg
    return AQI_LEVELS[-1][1:]


# ─────────────────────────────────────────────
# SAFE FLOAT
# ─────────────────────────────────────────────
def safe(v, default=0.0):
    try:
        return float(v)
    except:
        return default


# ─────────────────────────────────────────────
# FEATURE ENGINE (FIXED + SAFE)
# ─────────────────────────────────────────────
FEATURE_COLUMNS = model.feature_names_in_


def build_features(pm25, pm10, co, no2, o3, so2, nh3, temp, hum):
    row = {col: 0 for col in FEATURE_COLUMNS}

    now = datetime.now()

    base = {
        "pm2_5": pm25,
        "pm10": pm10,
        "co": co,
        "no2": no2,
        "o3": o3,
        "so2": so2,
        "nh3": nh3,
        "temp_c": temp,
        "humidity": hum,
    }

    for k, v in base.items():
        if k in row:
            row[k] = v

    row["hour"] = now.hour
    row["day"] = now.day
    row["weekday"] = now.weekday()
    row["month"] = now.month

    return pd.DataFrame([row])[FEATURE_COLUMNS]


# ─────────────────────────────────────────────
# PREDICT
# ─────────────────────────────────────────────
def predict_aqi(pm25, pm10, co, no2, o3, so2, nh3, temp, hum):
    df = build_features(pm25, pm10, co, no2, o3, so2, nh3, temp, hum)
    pred = model.predict(df)[0]
    return int(round(pred))


# ─────────────────────────────────────────────
# SAVE DATA
# ─────────────────────────────────────────────
def save_live_data(pm25, pm10, co, no2, o3, so2, nh3, temp, hum, aqi):
    row = pd.DataFrame([{
        "timestamp": datetime.now().isoformat(),
        "pm2_5": pm25,
        "pm10": pm10,
        "co": co,
        "no2": no2,
        "o3": o3,
        "so2": so2,
        "nh3": nh3,
        "temp": temp,
        "humidity": hum,
        "aqi": aqi,
    }])

    file = "dataset.csv"

    if os.path.exists(file):
        old = pd.read_csv(file)
        pd.concat([old, row], ignore_index=True).to_csv(file, index=False)
    else:
        row.to_csv(file, index=False)


# ─────────────────────────────────────────────
# FETCH DATA (SAFE)
# ─────────────────────────────────────────────
try:
    weather = get_weather_data()
    aqi_data = get_live_aqi()
except:
    weather = {}
    aqi_data = {}


pm25 = safe(aqi_data.get("pm25", 50))
pm10 = safe(aqi_data.get("pm10", 80))
co   = safe(aqi_data.get("co", 400))
no2  = safe(aqi_data.get("no2", 20))
o3   = safe(aqi_data.get("o3", 25))
so2  = safe(aqi_data.get("so2", 10))
nh3  = safe(aqi_data.get("nh3", 5))

temp = safe(weather.get("temp", 30))
hum  = safe(weather.get("humidity", 60))


# ─────────────────────────────────────────────
# COMPUTE AQI
# ─────────────────────────────────────────────
aqi = predict_aqi(pm25, pm10, co, no2, o3, so2, nh3, temp, hum)
label, color, msg = get_level(aqi)

save_live_data(pm25, pm10, co, no2, o3, so2, nh3, temp, hum, aqi)


# ─────────────────────────────────────────────
# ALERT SYSTEM
# ─────────────────────────────────────────────
if "alert_sent" not in st.session_state:
    st.session_state.alert_sent = False

if aqi >= 100 and not st.session_state.alert_sent:
    send_email_alert(aqi, label)
    send_sms_alert(aqi, label)
    st.session_state.alert_sent = True

if aqi < 100:
    st.session_state.alert_sent = False

# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
st.title("🌍 PolluCast Live Dashboard")
st.caption("AI-powered real-time air quality monitoring")


# ─────────────────────────────────────────────
# METRICS
# ─────────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)

col1.metric("AQI", aqi)
col2.metric("Category", label)
col3.metric("Temperature", f"{temp:.1f} °C")
col4.metric("Humidity", f"{hum:.0f} %")


# ─────────────────────────────────────────────
# HEALTH MESSAGE
# ─────────────────────────────────────────────
st.markdown(f"""
### 🩺 Health Advisory
<div style="padding:15px;background:{color}22;border-left:5px solid {color};border-radius:10px">
{msg}
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ═════════════════════════════════════════════
# NEW: CHARTS SECTION
# ═════════════════════════════════════════════

# ─────────────────────────────────────────────
# ROW 1: AQI GAUGE  +  POLLUTANTS BAR CHART
# ─────────────────────────────────────────────
chart_col1, chart_col2 = st.columns([1, 2])

with chart_col1:
    st.subheader("🎯 AQI Gauge")

    gauge_fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=aqi,
        delta={"reference": 100, "increasing": {"color": "#C0392B"}, "decreasing": {"color": "#16A37F"}},
        gauge={
            "axis": {"range": [0, 500], "tickwidth": 1, "tickcolor": "#555"},
            "bar": {"color": color},
            "steps": [
                {"range": [0, 50],   "color": "#D4EFDF"},
                {"range": [50, 100], "color": "#FCF3CF"},
                {"range": [100, 150],"color": "#FAD7A0"},
                {"range": [150, 200],"color": "#F1948A"},
                {"range": [200, 300],"color": "#C39BD3"},
                {"range": [300, 500],"color": "#F1948A"},
            ],
            "threshold": {
                "line": {"color": "#8B0000", "width": 3},
                "thickness": 0.75,
                "value": 100,
            },
        },
        title={"text": f"<b>{label}</b>", "font": {"size": 18}},
    ))
    gauge_fig.update_layout(height=300, margin=dict(t=40, b=10, l=20, r=20))
    st.plotly_chart(gauge_fig, use_container_width=True)

with chart_col2:
    st.subheader("☁️ Pollutant Levels")

    pollutants = {
        "PM2.5": pm25,
        "PM10":  pm10,
        "NO2":   no2,
        "O3":    o3,
        "SO2":   so2,
        "NH3":   nh3,
        "CO":    co,
    }

    # Color bars by severity (rough WHO thresholds)
    thresholds = {"PM2.5": 25, "PM10": 50, "NO2": 40, "O3": 100, "SO2": 20, "NH3": 200, "CO": 4000}
    bar_colors = [
        "#C0392B" if v > thresholds.get(k, 9999) else "#16A37F"
        for k, v in pollutants.items()
    ]

    bar_fig = go.Figure(go.Bar(
        x=list(pollutants.keys()),
        y=list(pollutants.values()),
        marker_color=bar_colors,
        text=[f"{v:.1f}" for v in pollutants.values()],
        textposition="outside",
    ))
    bar_fig.update_layout(
        height=300,
        margin=dict(t=20, b=20, l=10, r=10),
        yaxis_title="Concentration (µg/m³ or ppb)",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor="#E5E5E5"),
    )
    st.plotly_chart(bar_fig, use_container_width=True)


# ─────────────────────────────────────────────
# ROW 2: AQI TREND  +  TEMP & HUMIDITY TREND
# (from real CSV history — last 30 records)
# ─────────────────────────────────────────────
st.markdown("### 📈 Historical Trends (from logged data)")

trend_col1, trend_col2 = st.columns(2)

# Load CSV history
history_df = None
if os.path.exists("dataset.csv"):
    try:
        history_df = pd.read_csv("dataset.csv")
        history_df["timestamp"] = pd.to_datetime(history_df["timestamp"])
        history_df = history_df.tail(30)
    except:
        history_df = None

with trend_col1:
    st.subheader("🌫️ AQI Over Time")

    if history_df is not None and len(history_df) > 1:
        aqi_fig = go.Figure()
        aqi_fig.add_trace(go.Scatter(
            x=history_df["timestamp"],
            y=history_df["aqi"],
            mode="lines+markers",
            name="AQI",
            line=dict(color=color, width=2),
            marker=dict(size=5),
            fill="tozeroy",
            fillcolor=f"{color}22",
        ))
        # Danger threshold line
        aqi_fig.add_hline(
            y=100,
            line_dash="dash",
            line_color="#C0392B",
            annotation_text="Alert threshold (100)",
            annotation_position="top left",
        )
        aqi_fig.update_layout(
            height=280,
            margin=dict(t=10, b=20, l=10, r=10),
            yaxis=dict(range=[0, 500], title="AQI", gridcolor="#E5E5E5"),
            xaxis=dict(title="Time", showgrid=False),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(aqi_fig, use_container_width=True)
    else:
        # Fallback: simulated trend (original behaviour)
        hours = list(range(24))
        trend = [max(0, min(500, aqi + np.random.randint(-30, 30))) for _ in hours]
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=hours, y=trend, mode="lines", line=dict(color=color)))
        fig.update_layout(height=280, margin=dict(t=10, b=20, l=10, r=10),
                          xaxis_title="Hour", yaxis_title="AQI (simulated)",
                          plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True)
        st.caption("ℹ️ Showing simulated trend — more data will appear after a few refresh cycles.")

with trend_col2:
    st.subheader("🌡️ Temperature & Humidity Over Time")

    if history_df is not None and len(history_df) > 1:
        th_fig = go.Figure()
        th_fig.add_trace(go.Scatter(
            x=history_df["timestamp"],
            y=history_df["temp"],
            mode="lines+markers",
            name="Temperature (°C)",
            line=dict(color="#E74C3C", width=2),
            marker=dict(size=5),
            yaxis="y1",
        ))
        th_fig.add_trace(go.Scatter(
            x=history_df["timestamp"],
            y=history_df["humidity"],
            mode="lines+markers",
            name="Humidity (%)",
            line=dict(color="#2980B9", width=2, dash="dot"),
            marker=dict(size=5),
            yaxis="y2",
        ))
        th_fig.update_layout(
            height=280,
            margin=dict(t=10, b=20, l=10, r=10),
            yaxis=dict(title="Temperature (°C)", color="#E74C3C", gridcolor="#E5E5E5"),
            yaxis2=dict(title="Humidity (%)", color="#2980B9", overlaying="y", side="right", showgrid=False),
            xaxis=dict(title="Time", showgrid=False),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(th_fig, use_container_width=True)
    else:
        st.info("Temperature & humidity history will appear after a few refresh cycles.")


# ─────────────────────────────────────────────
# ROW 3: PM2.5 & PM10 TREND
# ─────────────────────────────────────────────
if history_df is not None and len(history_df) > 1:
    st.subheader("💨 PM2.5 & PM10 Trend")

    pm_fig = go.Figure()
    pm_fig.add_trace(go.Scatter(
        x=history_df["timestamp"],
        y=history_df["pm2_5"],
        mode="lines+markers",
        name="PM2.5",
        line=dict(color="#8E44AD", width=2),
        marker=dict(size=5),
        fill="tozeroy",
        fillcolor="rgba(142,68,173,0.1)",
    ))
    pm_fig.add_trace(go.Scatter(
        x=history_df["timestamp"],
        y=history_df["pm10"],
        mode="lines+markers",
        name="PM10",
        line=dict(color="#D35400", width=2),
        marker=dict(size=5),
        fill="tozeroy",
        fillcolor="rgba(211,84,0,0.08)",
    ))
    # WHO guideline lines
    pm_fig.add_hline(y=25, line_dash="dash", line_color="#8E44AD",
                     annotation_text="PM2.5 WHO limit (25)", annotation_position="top left")
    pm_fig.add_hline(y=50, line_dash="dash", line_color="#D35400",
                     annotation_text="PM10 WHO limit (50)", annotation_position="top right")
    pm_fig.update_layout(
        height=280,
        margin=dict(t=10, b=20, l=10, r=10),
        yaxis=dict(title="µg/m³", gridcolor="#E5E5E5"),
        xaxis=dict(title="Time", showgrid=False),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
    )
    st.plotly_chart(pm_fig, use_container_width=True)

st.markdown("---")

# ═════════════════════════════════════════════
# ORIGINAL SECTIONS (UNCHANGED)
# ═════════════════════════════════════════════

# ─────────────────────────────────────────────
# POLLUTANTS (raw values table)
# ─────────────────────────────────────────────
st.subheader("☁ Pollutants")

st.write({
    "PM2.5": pm25,
    "PM10": pm10,
    "CO": co,
    "NO2": no2,
    "O3": o3,
    "SO2": so2,
    "NH3": nh3
})


# ─────────────────────────────────────────────
# DATASET
# ─────────────────────────────────────────────
if os.path.exists("dataset.csv"):
    df = pd.read_csv("dataset.csv")
    st.subheader("📊 Dataset")
    st.dataframe(df.tail(10))
    st.download_button("Download CSV", df.to_csv(index=False), "dataset.csv")