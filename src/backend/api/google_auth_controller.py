from fastapi import APIRouter, Request
from api.google_auth_service import callback_google_auth, get_calendar_service, get_google_auth_url


class GoogleAuthController:    
    def __init__(self):
        pass

    def get_auth_status(self, user_id: str):
        """Verifica se o usuário está autenticado com o Google Calendar"""
        try:
            get_calendar_service(user_id)
            return {"authenticated": True, "message": "Usuário autenticado"}
        except Exception as e:
            return {
                "authenticated": False,
                "message": f"Usuário não autenticado {str(e)}",
            }

    def get_url_auth(self, user_id: str):
        """Retorna a URL de autenticação do Google"""
        try:
            auth_url = get_google_auth_url(user_id)

            return {"auth_url": auth_url}
        except Exception as e:
            return {"error": f"Erro ao gerar URL de autenticação: {str(e)}"}

    def google_callback(self, request: Request, state: str):
        """Callback do Google OAuth"""
        try:
            url = request.url
            callback_google_auth(url, state)
            return {
                "message": "Autenticação realizada com sucesso! Você pode fechar esta aba.",
                "authenticated": True,
            }
        except Exception as e:
            return {"error": f"Erro na autenticação: {str(e)}"}


def google_auth_router(controller: GoogleAuthController) -> APIRouter:
    router = APIRouter(prefix="/auth/google")

    @router.get("/status/{user_id}")
    async def get_auth_status(user_id: str):
        return controller.get_auth_status(user_id)

    @router.get("/url-auth/{user_id}")
    async def get_url_auth(user_id: str):
        return controller.get_url_auth(user_id)

    @router.get("/callback")
    async def google_callback(request: Request, state: str):
        return controller.google_callback(request, state)

    return router
