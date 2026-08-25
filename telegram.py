import httpx

from config import config
from response import Res

class Telegram:
    def __init__(self):
        self.token = config.TELEGRAM_BOT_TOKEN
        self.chat_id = config.TELEGRAM_CHAT_ID
        self.base_url = f"https://api.telegram.org/bot{self.token}"

    async def send(
        self,
        message: str,
        chat_id: str | None = None,
    ):
        chat_id = chat_id or self.chat_id
        if not chat_id:
            raise ValueError("Telegram chat_id belum dikonfigurasi")
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/sendMessage",
                json={
                    "chat_id": chat_id,
                    "text": message,
                    "parse_mode": "HTML",
                },
                timeout=10,
            )
            response.raise_for_status()
            return response.json()

    async def get_updates(self):
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/getUpdates",
                timeout=10,
            )

            response.raise_for_status()

            return response.json()

    async def handle_update(self, update: dict):
        message = update.get("message")

        if not message:
            return

        text = message.get("text", "")
        chat_id = message["chat"]["id"]

        if text == "/start":
            await self.send(
                "Bot aktif 🟢",
                chat_id=chat_id,
            )

        elif text == "/status":
            await self.send(
                "Server aman 🟢",
                chat_id=chat_id,
            )


tele = Telegram()