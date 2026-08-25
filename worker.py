import json

from workers import WorkerEntrypoint, Response, fetch

from app.core.response import Res
from app.core.telegram import tele_core


def json_response(data, status=200):
    return Response(
        json.dumps(data),
        status=status,
        headers={
            "content-type": "application/json",
        },
    )


class Default(WorkerEntrypoint):

    @property
    def base_url(self):
        return (
            f"https://api.telegram.org/"
            f"bot{self.env.TELEGRAM_BOT_TOKEN}"
        )

    async def fetch(self, request):
        url = request.url
        path = "/" + url.split("/", 3)[-1] if url.count("/") >= 3 else "/"

        # ROOT
        if request.method == "GET" and path == "/":
            return json_response(
                Res.ok({
                    "service": "telegram-bot",
                    "runtime": "cloudflare-worker",
                })
            )

        # TEST
        if request.method == "GET" and path == "/test":
            result = await self._send(
                text=(
                    "🟢 <b>Telegram Bot</b>\n"
                    "Service Cloudflare Worker berhasil terhubung."
                )
            )
            return json_response(Res.ok(result,"Pesan berhasil dikirim",))

        # LIST CHAT
        if request.method == "GET" and path == "/chats":
            return await self.chats()

        # OPEN BOT
        if request.method == "GET" and path == "/open":
            return Response.redirect(
                f"https://t.me/{self.env.TELEGRAM_BOT_USERNAME}?start=server1",
                302,
            )

        # SEND MESSAGE
        if request.method == "POST" and path == "/send":
            return await self.send(request)

        # TELEGRAM WEBHOOK
        if request.method == "POST" and path == "/webhook":
            return await self.webhook(request)

        return json_response(Res.error("Not Found", 404),404,)

    async def _send(self,text: str,chat_id=None,):
        chat_id = chat_id or self.env.TELEGRAM_CHAT_ID
        payload = tele_core._payload(chat_id=chat_id,text=text,)

        response = await fetch(
            f"{self.base_url}/sendMessage",
            method="POST",
            headers={
                "content-type": "application/json",
            },
            body=json.dumps(payload),
        )
        return await response.json()

    async def send(self, request):
        data = await request.json()
        message = data.get("message")
        chat_id = data.get("chat_id")
        if not message:
            return json_response(
                Res.error("message wajib diisi",400,),
                400,
            )

        result = await self._send(text=message,chat_id=chat_id,)
        return json_response(
            Res.ok(result,"Pesan berhasil dikirim",)
        )

    async def chats(self):
        response = await fetch(
            f"{self.base_url}/getUpdates"
        )
        data = await response.json()
        chats = {}
        for update in data.get("result", []):
            message = update.get("message")
            if not message:
                continue
            chat = message.get("chat", {})
            user = message.get("from", {})
            chat_id = chat.get("id")
            if not chat_id:
                continue
            # Biar chat yang sama tidak muncul berkali-kali
            chats[str(chat_id)] = {
                "chat_id": chat_id,
                "type": chat.get("type"),
                "username": user.get("username"),
                "first_name": user.get("first_name"),
            }
        return json_response(
            Res.ok(
                list(chats.values()),
                "Daftar chat berhasil diambil",
            )
        )

    async def webhook(self, request):
        update = await request.json()
        data = tele_core._update(update)
        if not data:
            return json_response(Res.ok(message="Update diabaikan"))
        reply = tele_core._command(data["text"])
        if reply:
            await self._send(text=reply,chat_id=data["chat_id"],)

        return json_response(Res.ok(message="Update diterima"))