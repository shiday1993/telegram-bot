from fastapi import FastAPI, Request, Header, HTTPException

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