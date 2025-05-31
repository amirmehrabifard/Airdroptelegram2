
import os
import requests

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

def set_webhook():
    if not BOT_TOKEN or not WEBHOOK_URL:
        raise ValueError("BOT_TOKEN or WEBHOOK_URL not set in environment variables.")

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook"
    data = {"url": f"{WEBHOOK_URL}/{BOT_TOKEN}"}

    response = requests.post(url, data=data)
    print(response.json())

if __name__ == "__main__":
    set_webhook()
