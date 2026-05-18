import pandas as pd
import joblib

# ---------------- LOAD MODEL ----------------

model = joblib.load("model.pkl")

# ---------------- FEATURE ORDER ----------------

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

# ---------------- PREDICTION FUNCTION ----------------

def predict_aqi(input_data):

    df = pd.DataFrame([input_data])

    # IMPORTANT: FORCE SAME COLUMN ORDER
    df = df[FEATURE_COLUMNS]

    prediction = model.predict(df)[0]

    return round(prediction, 2)

# ---------------- HEALTH STATUS ----------------

def get_aqi_status(aqi):

    if aqi <= 50:
        return "😊 Good Air Quality"

    elif aqi <= 100:
        return "😐 Moderate Air Quality"

    elif aqi <= 150:
        return "⚠️ Unhealthy for Sensitive Groups"

    elif aqi <= 200:
        return "🚨 Unhealthy"

    elif aqi <= 300:
        return "☠️ Very Unhealthy"

    else:
        return "💀 Hazardous"