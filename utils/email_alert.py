import smtplib
import streamlit as st
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email_alert(aqi, level):

    try:
        sender_email = st.secrets["EMAIL_USER"]
        sender_password = st.secrets["EMAIL_PASS"]

        receiver_email = st.secrets.get(
            "ALERT_EMAIL",
            sender_email
        )

        subject = f"🌍 PolluCast AQI Alert - {level}"

        body = f"""
<html>
<body style="margin:0;padding:0;background:#0b0f14;font-family:Arial">

<div style="max-width:600px;margin:auto;padding:25px;">

    <!-- CARD -->
    <div style="
        background:#111827;
        border-radius:18px;
        padding:25px;
        box-shadow:0 10px 25px rgba(0,0,0,0.4);
        border:1px solid #1f2937;
    ">

        <!-- HEADER -->
        <h1 style="color:#00ffcc;text-align:center;margin-bottom:10px;">
            🌍 PolluCast Alert
        </h1>

        <p style="text-align:center;color:#9ca3af;margin-top:0;">
            Real-Time Air Quality Notification
        </p>

        <hr style="border:0;border-top:1px solid #222;margin:20px 0;">

        <!-- AQI BOX -->
        <div style="
            text-align:center;
            padding:20px;
            background:#0f172a;
            border-radius:12px;
        ">
            <h2 style="color:#ffffff;margin:0;">AQI Level</h2>
            <p style="font-size:40px;margin:10px 0;color:#00d4ff;">
                {aqi}
            </p>
            <p style="color:#fbbf24;font-size:18px;">
                {level}
            </p>
        </div>

        <!-- MESSAGE -->
        <p style="color:#d1d5db;margin-top:20px;line-height:1.6;text-align:center;">
            ⚠️ Air quality has reached a critical level.<br>
            Please avoid outdoor activities and stay safe.
        </p>

        <!-- FOOTER -->
        <div style="
            margin-top:25px;
            text-align:center;
            font-size:12px;
            color:#6b7280;
        ">
            PolluCast • AI-powered Air Quality Monitoring System
        </div>

    </div>

</div>

</body>
</html>
"""
        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = receiver_email
        msg["Subject"] = subject

        msg.attach(MIMEText(body, "html"))

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()

        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()

        print("EMAIL SENT ✅")

    except Exception as e:
        print("EMAIL FAILED ❌", e)