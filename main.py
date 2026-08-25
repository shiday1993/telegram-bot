from fastapi import FastAPI, Request, Header, HTTPException

from app.config import config
from app.telegram import tele
from app.response import Res


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
async def test():
    try:
        result = await tele.send(
            "🟢 <b>Telegram Bot</b>\n"
            "Service berhasil terhubung."
        )

        return Res.ok(
            data=result,
            message="Pesan berhasil dikirim",
        )

    except Exception as e:
        return Res.error(
            message=str(e),
            code=500,
        )


@app.get("/updates")
async def updates():
    data = await tele.get_updates()

    chats = []

    for update in data.get("result", []):
        message = update.get("message")

        if not message:
            continue

        chat = message.get("chat", {})
        user = message.get("from", {})

        chats.append({
            "chat_id": chat.get("id"),
            "type": chat.get("type"),
            "username": user.get("username"),
            "first_name": user.get("first_name"),
            "text": message.get("text"),
        })

    return chats


@app.post("/webhook")
async def telegram_webhook(
    request: Request,
    x_telegram_bot_api_secret_token: str | None = Header(default=None),
):
    if (
        config.TELEGRAM_WEBHOOK_SECRET
        and x_telegram_bot_api_secret_token
        != config.TELEGRAM_WEBHOOK_SECRET
    ):
        raise HTTPException(
            status_code=403,
            detail="Invalid webhook secret",
        )

    update = await request.json()

    await tele.handle_update(update)

    return Res.oke({
        "ok": True,
    })