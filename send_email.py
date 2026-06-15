"""
Wedding Countdown Email — Daily Sender
"""

import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import date
import os


# ── CONFIG — only change these ────────────────────────────────────────────────
WEDDING_DATE   = date(2026, 12, 27)          # your wedding date
YOUR_NAME      = "MM"                 # your name
HIS_NAME       = "Amogh"                  # your fiancé's name
FROM_EMAIL     = os.environ.get("FROM_EMAIL")
APP_PASSWORD   = os.environ.get("GMAIL_PASSWORD")
TO_EMAIL       = os.environ.get("TO_EMAIL")
COUNTDOWN_URL = "https://meghanamirji.github.io/wedding-countdown/"
# ─────────────────────────────────────────────────────────────────────────────

def days_left():
    delta = WEDDING_DATE - date.today()
    return max(0, delta.days)

def pick_emoji(n):
    if n > 100: return "🗓️"
    if n > 30:  return "🌸"
    if n > 14:  return "💐"
    if n > 7:   return "💍"
    if n > 1:   return "✨"
    if n == 1:  return "🥹"
    return "🎊"

def build_email(n):
    emoji = pick_emoji(n)

    if n == 0:
        subject = f"Today is the day, {HIS_NAME}! 🎊"
        body_text = "No countdown left. Just us, and a lifetime ahead."
    elif n == 1:
        subject = f"Tomorrow, {HIS_NAME}. Just one more sleep. 🥹"
        body_text = "One more sleep. Then forever starts."
    else:
        subject = f"{emoji} {n} days until our wedding, {HIS_NAME}"
        body_text = f"Every morning I wake up and think — in {n} days, I get to marry you."

    html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<style>
  body {{ margin:0; padding:0; background:#fdfaf8; font-family:'Georgia',serif; }}
  .wrap {{ max-width:520px; margin:0 auto; padding:48px 24px; text-align:center; }}
  .rule {{ width:1px; height:48px; background:linear-gradient(to bottom,transparent,#c9a96e);
           margin:0 auto 32px; }}
  .eyebrow {{ font-family:Arial,sans-serif; font-weight:300; font-size:10px;
              letter-spacing:0.35em; text-transform:uppercase; color:#9a7f8e;
              margin-bottom:24px; }}
  .big {{ font-size:clamp(56px,15vw,90px); font-weight:300; color:#c47f9a;
          line-height:1; margin-bottom:8px; font-style:italic; }}
  .unit {{ font-family:Arial,sans-serif; font-size:13px; letter-spacing:0.25em;
           text-transform:uppercase; color:#9a7f8e; margin-bottom:32px; }}
  .divider {{ border:none; border-top:0.5px solid #c9a96e; opacity:0.4;
              width:60px; margin:0 auto 28px; }}
  .note {{ font-size:18px; font-style:italic; line-height:1.7; color:#2e1f2b;
           margin-bottom:36px; font-weight:300; }}
  .btn {{ display:inline-block; padding:13px 34px;
          background:#c47f9a; color:#fff; text-decoration:none;
          font-family:Arial,sans-serif; font-size:12px; letter-spacing:0.25em;
          text-transform:uppercase; border-radius:40px; }}
  .footer {{ margin-top:40px; font-family:Arial,sans-serif; font-size:11px;
             color:#c9a96e; letter-spacing:0.2em; text-transform:uppercase; }}
  .rule-b {{ width:1px; height:36px; background:linear-gradient(to top,transparent,#c9a96e);
             margin:24px auto 0; }}
</style>
</head>
<body>
<div class="wrap">
  <div class="rule"></div>
  <p class="eyebrow">days until our wedding</p>
  <div class="big">{n if n > 0 else "✦"}</div>
  <p class="unit">{"days" if n != 1 else "day"} to go</p>
  <hr class="divider" />
  <p class="note">{body_text}</p>
  <a href="{COUNTDOWN_URL}" class="btn">open your message ✦</a>
  <p class="footer">{YOUR_NAME} &nbsp;·&nbsp; always yours</p>
  <div class="rule-b"></div>
</div>
</body>
</html>
"""
    return subject, html


def send():
    n = days_left()
    subject, html_body = build_email(n)

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"]    = f"{YOUR_NAME} 💍 <{FROM_EMAIL}>"
    msg["To"]      = TO_EMAIL

    plain = f"{subject}\n\nOpen your message: {COUNTDOWN_URL}"
    msg.attach(MIMEText(plain, "plain"))
    msg.attach(MIMEText(html_body, "html"))

    ctx = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=ctx) as server:
        server.login(FROM_EMAIL, APP_PASSWORD)
        server.sendmail(FROM_EMAIL, TO_EMAIL, msg.as_string())

    print(f"✓ Email sent — {n} days to go!")


if __name__ == "__main__":
    send()
