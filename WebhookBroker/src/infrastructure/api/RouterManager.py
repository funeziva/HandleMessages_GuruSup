from infrastructure.api.Email.EmailController import EmailRouter

class RouterManager:
    @classmethod
    def create_routes(cls, app):
        app.include_router(EmailRouter)