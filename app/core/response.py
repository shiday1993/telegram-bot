from fastapi.responses import JSONResponse
from typing import Optional, Dict, Any

class Res:
    @staticmethod
    def ok(
        data: Optional[dict] = None,
        message: str = "OK",
        response=None,
        code: int = 200
    ):
        body = {
            "metaData": {
                "code": code,
                "message": message
            },
            "response": data or {}
        }

        if response:
            response.status_code = code
            return body

        return JSONResponse(status_code=code, content=body)

    @staticmethod
    def fail(
        message: str = "Gagal",
        code: int = 400,
        data: Optional[dict] = None
    ):
        return JSONResponse(
            status_code=code,
            content={
                "metaData": {
                    "code": code,
                    "message": message
                },
                "response": data or {}
            }
        )

    @staticmethod
    def error(message: str = "Internal Server Error"):
        return JSONResponse(
            status_code=500,
            content={
                "metaData": {
                    "code": 500,
                    "message": message
                }
            }
        )

    @staticmethod
    def not_found(message="Data tidak ditemukan"):
        return JSONResponse(
            status_code=404,
            content={
                "metaData": {
                    "code": 404,
                    "message": message
                }
            }
        )

    @staticmethod
    def validation(errors=None, message="Validasi gagal"):
        return JSONResponse(
            status_code=422,
            content={
                "metaData": {
                    "code": "422",
                    "message": message
                },
                "response": errors
            }
        )

