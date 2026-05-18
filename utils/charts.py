import plotly.express as px

# ---------------- AQI CHART ----------------

def create_aqi_chart(df):

    fig = px.line(
        df,
        x="timestamp_ist",
        y="AQI",
        title="AQI Trend Analysis"
    )

    return fig

# ---------------- TEMPERATURE CHART ----------------

def create_temp_chart(df):

    fig = px.line(
        df,
        x="timestamp_ist",
        y="temp_c",
        title="Temperature Trend"
    )

    return fig