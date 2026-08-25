import os
from dotenv import load_dotenv

load_dotenv()


def get_str(key, default=None):
    return os.getenv(key, default)


def get_int(key, default=0):
    try:
        return int(os.getenv(key, default))
    except (TypeError, ValueError):
        return default


class Settings:
    APP_HOST = get_str("APP_HOST", "0.0.0.0")
    APP_PORT = get_int("APP_PORT", 8000)

    TELEGRAM_BOT_TOKEN = get_str("TELEGRAM_BOT_TOKEN")
    TELEGRAM_CHAT_ID = get_str("TELEGRAM_CHAT_ID")
    TELEGRAM_WEBHOOK_SECRET = get_str("TELEGRAM_WEBHOOK_SECRET")


config = Settings()