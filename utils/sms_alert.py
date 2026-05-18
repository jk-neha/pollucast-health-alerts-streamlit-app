from twilio.rest import Client
import streamlit as st

def send_sms_alert(aqi, level):
    try:
        client = Client(
            st.secrets["TWILIO_ACCOUNT_SID"],
            st.secrets["TWILIO_AUTH_TOKEN"]
        )

        message = f"🚨 PolluCast AQI ALERT!\nAQI: {aqi}\nLevel: {level}"

        client.messages.create(
            body=message,
            from_=st.secrets["TWILIO_SMS_NUMBER"],
            to=st.secrets["MY_PHONE_NUMBER"]
        )

        print("SMS sent successfully!")

    except Exception as e:
        print("SMS failed:", e)