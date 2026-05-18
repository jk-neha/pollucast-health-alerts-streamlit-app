import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import streamlit as st
import smtplib
import streamlit as st

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email_alert(aqi, level):

    sender_email = st.secrets["EMAIL_USER"]

    sender_password = st.secrets["EMAIL_PASS"]

    receiver_email = "jknehavardhini2004@gmail.com"

    subject = f"🌍 PolluCast AQI Alert - {level}"

    # HTML EMAIL BODY
    body = f"""
    <html>
    <body style="
        background-color:#0D0D0D;
        color:white;
        font-family:Arial;
        padding:30px;
    ">

        <div style="
            max-width:600px;
            margin:auto;
            background:#161616;
            border-radius:20px;
            padding:30px;
            border:1px solid #2A2A2A;
        ">

            <h1 style="
                color:#00FFA3;
                text-align:center;
            ">
                🌍 PolluCast Alert
            </h1>

            <hr style="border:1px solid #222;">

            <h2>
                AQI Level:
                <span style="color:#00C2FF;">
                    {aqi}
                </span>
            </h2>

            <h2>
                Condition:
                <span style="color:#FFC857;">
                    {level}
                </span>
            </h2>

            <p style="
                margin-top:25px;
                font-size:16px;
                line-height:1.7;
                color:#CCCCCC;
            ">
                Please stay safe and avoid outdoor exposure
                if the air quality becomes unhealthy.
            </p>

            <div style="
                margin-top:30px;
                padding:15px;
                background:#101010;
                border-radius:12px;
                text-align:center;
                color:#777;
                font-size:13px;
            ">
                PolluCast • AI Powered Air Quality Monitoring
            </div>

        </div>

    </body>
    </html>
    """

    try:

        # CREATE MESSAGE
        msg = MIMEMultipart("alternative")

        msg["Subject"] = subject

        msg["From"] = sender_email

        msg["To"] = receiver_email

        # ATTACH HTML
        msg.attach(MIMEText(body, "html"))

        # SMTP SERVER
        server = smtplib.SMTP("smtp.gmail.com", 587)

        server.starttls()

        # LOGIN
        server.login(
            sender_email,
            sender_password
        )

        # SEND EMAIL
        server.sendmail(
            sender_email,
            receiver_email,
            msg.as_string()
        )

        server.quit()

        print("EMAIL SENT SUCCESSFULLY ✅")

    except Exception as e:

        print("EMAIL ERROR ❌")

        print(e)


import streamlit as st

def send_email_alert(aqi, level):
    if "EMAIL_USER" not in st.secrets or "EMAIL_PASS" not in st.secrets:
        print("Email secrets not configured. Skipping alert.")
        return

    sender_email = st.secrets["EMAIL_USER"]
    sender_password = st.secrets["EMAIL_PASS"]