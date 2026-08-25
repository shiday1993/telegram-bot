from fastapi.responses import JSONResponse


class Res:
    @staticmethod
    def ok(data=None, message="OK", code=200):
        return JSONResponse(
            status_code=code,
            content={
                "metaData": {
                    "code": code,
                    "message": message,
                },
                "response": data,
            },
        )

    @staticmethod
    def error(message="Server Error", code=500):
        return JSONResponse(
            status_code=code,
            content={
                "metaData": {
                    "code": code,
                    "message": message,
                },
                "response": None,
            },
        )