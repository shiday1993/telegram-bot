from fastapi import FastAPI, Request, Header, HTTPException

from config import config
from telegram import send_message


app = FastAPI(
    title="Telegram Bot",
    version="1.0.0",
)


@app.get("/")
def root():
    return {
        "status": "ok",
        "service": "telegram-bot",
    }


@app.get("/test")
def test():
    result = send_message(
        "🟢 <b>Telegram Bot</b>\n"
        "Service berhasil terhubung."
    )

    return {
        "success": bool(result),
        "telegram": result,
    }


@app.post("/webhook")
async def telegram_webhook(
    request: Request,
    x_telegram_bot_api_secret_token: str | None = Header(default=None),
):
    if config.TELEGRAM_WEBHOOK_SECRET:
        if (
            x_telegram_bot_api_secret_token
            != config.TELEGRAM_WEBHOOK_SECRET
        ):
            raise HTTPException(
                status_code=403,
                detail="Invalid webhook secret",
            )

    update = await request.json()

    print("Telegram Update:")
    print(update)

    return {
        "ok": True,
    }