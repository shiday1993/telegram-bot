import json

from workers import WorkerEntrypoint, Response


class Default(WorkerEntrypoint):
    async def fetch(self, request):
        url = request.url

        if request.method == "GET" and url.endswith("/"):
            return Response(
                json.dumps({
                    "metaData": {
                        "code": 200,
                        "message": "OK"
                    },
                    "response": {
                        "service": "telegram-notifier"
                    }
                }),
                headers={
                    "content-type": "application/json"
                }
            )

        return Response(
            json.dumps({
                "metaData": {
                    "code": 404,
                    "message": "Not Found"
                },
                "response": None
            }),
            status=404,
            headers={
                "content-type": "application/json"
            }
        )