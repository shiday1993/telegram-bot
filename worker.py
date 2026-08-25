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

    async def fetch(self, request):
        url = request.url
        path = "/" + url.split("/", 3)[-1] if url.count("/") >= 3 else "/"

        if request.method == "GET" and path == "/":
            return json_response(
                Res.ok({
                    "service": "telegram-bot",
                    "runtime": "cloudflare-worker",
                })
            )

        if request.method == "POST" and path == "/send":
            return await self.send(request)

        if request.method == "POST" and path == "/webhook":
            return await self.webhook(request)

        return json_response(
            Res.error("Not Found", 404),
            404,
        )

    async def send(self, request):
        data = await request.json()

        chat_id = data.get("chat_id") or self.env.TELEGRAM_CHAT_ID
        message = data.get("message")

        payload = tele_core.message_payload(
            chat_id=chat_id,
            text=message,
        )

        response = await fetch(
            f"https://api.telegram.org/bot{self.env.TELEGRAM_BOT_TOKEN}/sendMessage",
            method="POST",
            headers={
                "content-type": "application/json",
            },
            body=json.dumps(payload),
        )

        result = await response.json()

        return json_response(
            Res.ok(result)
        )

    async def webhook(self, request):
        update = await request.json()

        data = tele_core.parse_update(update)

        if not data:
            return json_response(Res.ok())

        reply = tele_core.handle_command(
            data["text"]
        )

        if reply:
            payload = tele_core.message_payload(
                chat_id=data["chat_id"],
                text=reply,
            )

            await fetch(
                f"https://api.telegram.org/bot{self.env.TELEGRAM_BOT_TOKEN}/sendMessage",
                method="POST",
                headers={
                    "content-type": "application/json",
                },
                body=json.dumps(payload),
            )

        return json_response(Res.ok())