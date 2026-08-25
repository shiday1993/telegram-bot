import httpx

from app.config import config
from app.core.telegram import tele_core as tele


class TelegramService:

    def __init__(self):
        self.token = config.TELEGRAM_BOT_TOKEN
        self.chat_id = config.TELEGRAM_CHAT_ID

    @property
    def base_url(self):
        return f"https://api.telegram.org/bot{self.token}"

    async def send(
        self,
        text: str,
        chat_id=None,
    ):
        payload = tele._payload(
            chat_id=chat_id or self.chat_id,
            text=text,
        )

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/sendMessage",
                json=payload,
                timeout=10,
            )

            response.raise_for_status()

            return response.json()

    async def handle_update(self, update: dict):
        data = tele._update(update)

        if not data:
            return None

        reply = tele._command(
            data["text"]
        )

        if reply:
            return await self.send(
                text=reply,
                chat_id=data["chat_id"],
            )

        return None


tele = TelegramService()