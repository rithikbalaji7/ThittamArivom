import os
import requests


SMS_API_URL = os.getenv("SMS_API_URL")
SMS_API_TOKEN = os.getenv("SMS_API_TOKEN")
SMS_SENDER = os.getenv("SMS_SENDER")


def send_sms(to: str, message: str):

    payload = {
        "to": to,
        "from": SMS_SENDER,
        "body": message
    }

    headers = {
        "Authorization": f"Bearer {SMS_API_TOKEN}",
        "Content-Type": "application/json"
    }

    response = requests.post(
        SMS_API_URL,
        json=payload,
        headers=headers,
        timeout=20
    )

    response.raise_for_status()

    return response.json()