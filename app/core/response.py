class Res:
    @staticmethod
    def ok(data=None, message="OK"):
        return {
            "metaData": {
                "code": 200,
                "message": message,
            },
            "response": data,
        }

    @staticmethod
    def error(message="Server Error", code=500):
        return {
            "metaData": {
                "code": code,
                "message": message,
            },
            "response": None,
        }