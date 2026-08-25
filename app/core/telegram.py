class TelegramCore:

    @staticmethod
    def _payload(
        chat_id,
        text: str,
        parse_mode: str = "HTML",
    ):
        return {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": parse_mode,
        }

    @staticmethod
    def _update(update: dict):
        message = update.get("message")

        if not message:
            return None

        user = message.get("from", {})
        chat = message.get("chat", {})

        return {
            "chat_id": chat.get("id"),
            "text": message.get("text", ""),
            "username": user.get("username"),
            "first_name": user.get("first_name"),
        }

    @staticmethod
    def _command(text: str):
        if text.startswith("/start"):
            parts = text.split(maxsplit=1)
            param = parts[1] if len(parts) > 1 else None
            if param == "server1":
                return "🟢 Kamu masuk dari Server 1"
            return "🟢 Bot aktif."  

        if text == "/status":
            return "🟢 Service berjalan normal."

        return None


tele_core = TelegramCore()