import os
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/calendar"]

temp_flows = {}

def _get_token_path(user_id: str):
    script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    token_path = os.path.join(script_dir, "access_tokens", f"{user_id}_token.json")
    return token_path


def get_calendar_service(user_id: str):
    """Autentica e retorna um objeto de serviço para interagir com a API."""

    token_path = _get_token_path(user_id)

    # credentials_path = os.path.join(script_dir, "google_client_secret.json")

    creds = None
    # Busca o token de acesso do usuário.
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)

    # Se não houver credenciais válidas, pede para o usuário fazer login.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            raise Exception("Permissão negada para acessar o Google Calendar")
            # flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
            # creds = flow.run_local_server(port=0)

        # Armazena o token de acesso do usuário.
        with open(token_path, "w") as token:
            token.write(creds.to_json())

    calendar_service = build("calendar", "v3", credentials=creds)

    return calendar_service


def callback_google_auth(url: str, user_id: str):
    """Callback do Google OAuth"""
    if user_id not in temp_flows:
        return {"error": "Sessão de autenticação expirada"}

    # Capturar o código de autorização da query string
    authorization_response = str(url)
    temp_flows[user_id].fetch_token(authorization_response=authorization_response)

    # Salvar as credenciais
    token_path = _get_token_path(user_id)
    os.makedirs(os.path.dirname(token_path), exist_ok=True)

    creds = temp_flows[user_id].credentials
    with open(token_path, "w") as token:
        token.write(creds.to_json())

    # Limpar o flow temporário
    del temp_flows[user_id]

def get_google_auth_url(user_id: str):
    """Retorna a URL de autenticação do Google"""
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    print(f"script_dir: {script_dir}")
    credentials_path = os.path.join(script_dir, "google_client_secret.json")

    flow = Flow.from_client_secrets_file(
        credentials_path,
        scopes=["https://www.googleapis.com/auth/calendar"],
        redirect_uri=f"http://localhost:5000/auth/google/callback/{user_id}",
    )

    auth_url, _ = flow.authorization_url(prompt="consent")

    # Armazenar o flow temporariamente (em produção, use Redis/DB)
    temp_flows[user_id] = flow 

    return auth_url