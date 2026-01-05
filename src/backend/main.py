from fastapi import FastAPI
import uvicorn
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

from api.google_auth_controller import GoogleAuthController, google_auth_router
from api.agent_flow_controller import AgentFlowController, agent_flow_router
from api.agent_flow_service import AgentFlowService

load_dotenv()

if not os.getenv("GOOGLE_API_KEY"):
    raise ValueError("GOOGLE_API_KEY não está definida")

APP_NAME = os.getenv("APP_NAME") or "EasyBooker"

app = FastAPI(
    title="EasyBooker",
    description="EasyBooker - Assistente Inteligente com Cadeia de Agentes de IA para Agendamento e Gestão de Compromissos",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://easybooker.djansantos.com.br",
        "https://easybooker.djansantos.com.br",
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# ROTAS
agent_flow_service = AgentFlowService()
agent_flow_controller = AgentFlowController(agent_flow_service)
google_auth_controller = GoogleAuthController()

agent_flow_router_api = agent_flow_router(agent_flow_controller)
google_auth_router_api = google_auth_router(google_auth_controller)


@app.get("/")
async def root():
    return {"message": "EasyBooker API is running"}


app.include_router(agent_flow_router_api)
app.include_router(google_auth_router_api)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000, access_log=True)
