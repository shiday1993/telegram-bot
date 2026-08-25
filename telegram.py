import requests

from config import config


class Telegram:
    def __init__(self):
        self.token = config.TELEGRAM_BOT_TOKEN
        self.chat_id = config.TELEGRAM_CHAT_ID
        self.base_url = f"https://api.telegram.org/bot{self.token}"

        print("TOKEN:", config.TELEGRAM_BOT_TOKEN[:8] if config.TELEGRAM_BOT_TOKEN else None)
        print("CHAT_ID:", config.TELEGRAM_CHAT_ID)
        
    def send(self, message: str, chat_id: str | None = None):
        chat_id = chat_id or self.chat_id
        response = requests.post(
            f"{self.base_url}/sendMessage",
            json={
                "chat_id": chat_id,
                "text": message,
                "parse_mode": "HTML",
            },
            timeout=10,
        )
        print("STATUS:", response.status_code)
        print("RESPONSE:", response.text)
        response.raise_for_status()
        return response.json()

    def handle_update(self, update: dict):
        message = update.get("message")

        if not message:
            return

        text = message.get("text", "")
        chat_id = message["chat"]["id"]

        if text == "/start":
            self.send(
                "Bot aktif 🟢",
                chat_id=chat_id,
            )

        elif text == "/status":
            self.send(
                "Server aman 🟢",
                chat_id=chat_id,
            )
            
    def get_updates(self):
        response = requests.get(
            f"{self.base_url}/getUpdates",
            timeout=10,
        )
        response.raise_for_status()
        return response.json()

tele = Telegram()