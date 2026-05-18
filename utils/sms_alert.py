from twilio.rest import Client
import streamlit as st

def send_sms_alert(aqi, level):
    account_sid = st.secrets["TWILIO_ACCOUNT_SID"]
    auth_token = st.secrets["TWILIO_AUTH_TOKEN"]
    twilio_number = st.secrets["TWILIO_SMS_NUMBER"]

    client = Client(account_sid, auth_token)

    message = f"🚨 AQI ALERT!\nAQI: {aqi}\nLevel: {level}\nPolluCast Health Warning!"

    client.messages.create(
        body=message,
        from_=twilio_number,
        to="+918122978440"   # 👈 replace with your phone number
    )