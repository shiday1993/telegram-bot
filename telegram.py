import requests

from config import config


BASE_URL = f"https://api.telegram.org/bot{config.TELEGRAM_BOT_TOKEN}"


def send_message(
    message: str,
    chat_id: str | None = None,
):
    chat_id = chat_id or config.TELEGRAM_CHAT_ID

    try:
        response = requests.post(
            f"{BASE_URL}/sendMessage",
            json={
                "chat_id": chat_id,
                "text": message,
                "parse_mode": "HTML",
            },
            timeout=10,
        )

        response.raise_for_status()

        data = response.json()

        return data

    except requests.RequestException as e:
        print(f"Telegram error: {e}")
        return None