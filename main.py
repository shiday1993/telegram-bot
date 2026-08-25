from fastapi import FastAPI, Request, Header, HTTPException
from fastapi.responses import RedirectResponse

from app.config import config
from app.service.telegram import tele_service
from app.core.response import Res


app = FastAPI(
    title="Telegram Bot",
    version="1.0.0",
)

@app.get("/")
async def root():
    return Res.ok({
        "service": "telegram-bot",
        "runtime": "fastapi",
    })


@app.get("/test")
async def test():
    try:
        result = await tele_service.send(
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

@app.post("/send")
async def send(request: Request):
    try:
        data = await request.json()
        result = await tele_service.send(
            text=data["message"],
            chat_id=data.get("chat_id"),
        )
        return Res.ok(result,"Pesan berhasil dikirim",)
    except Exception as e:
        return Res.error(str(e))


@app.post("/webhook")
async def webhook(request: Request):
    try:
        update = await request.json()
        await tele_service.handle_update(update)
        return Res.ok(message="Update diterima")
    except Exception as e:
        return Res.error(str(e))
    
@app.get("/chats")
async def chats():
    try:
        data = await tele_service.get_updates()
        result = {}
        for update in data.get("result", []):
            message = update.get("message")
            if not message:
                continue
            chat = message.get("chat", {})
            user = message.get("from", {})
            chat_id = chat.get("id")
            if not chat_id:
                continue

            result[chat_id] = {
                "chat_id": chat_id,
                "type": chat.get("type"),
                "username": user.get("username"),
                "first_name": user.get("first_name"),
            }

        return Res.ok(
            data=list(result.values()),
            message="Daftar chat berhasil diambil",
        )

    except Exception as e:
        return Res.error(
            message=str(e),
            code=500,
        )
        
@app.get("/start")
async def start_bot():
    return RedirectResponse(
        url=(
            f"https://t.me/"
            f"{config.TELEGRAM_BOT_USERNAME}"
            f"?start=web"
        )
    )