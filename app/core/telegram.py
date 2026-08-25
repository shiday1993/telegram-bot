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

        if not isinstance(message, dict):
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
    def _command(text: str, chat_id=None):
        if text.startswith("/start"):
            return (
                "🟢 <b>Bot aktif.</b>\n\n"
                f"🆔 Chat ID: <code>{chat_id}</code>"
            )

        if text == "/id":
            return (
                "🆔 <b>Chat ID</b>\n"
                f"<code>{chat_id}</code>"
            )

        if text == "/status":
            return (
                "🟢 <b>Service berjalan normal.</b>\n\n"
                f"Chat ID: <code>{chat_id}</code>"
            )

        return None



tele_core = TelegramCore()