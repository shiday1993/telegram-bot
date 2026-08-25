import os
from dotenv import load_dotenv

load_dotenv()


def get_str(key: str, default=None):
    return os.getenv(key, default)


class Config:
    APP_ENV = get_str("APP_ENV", "development")

    TELEGRAM_BOT_TOKEN = get_str("TELEGRAM_BOT_TOKEN")
    TELEGRAM_CHAT_ID = get_str("TELEGRAM_CHAT_ID")
    TELEGRAM_WEBHOOK_SECRET = get_str("TELEGRAM_WEBHOOK_SECRET")


config = Config()