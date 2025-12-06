
import json
import os
from agents.stt_agent.agent import stt_agent
from agents.npl_agent.agent import npl_agent
from agents.suggestor_agent.agent import suggestor_agent
from agents.scheduler_agent.agent import scheduler_agent
from agents.normalizer_agent.agent import normalizer_agent
from google.genai.types import Content, Part
from google.adk.runners import InMemoryRunner

APP_NAME = os.getenv("APP_NAME") or "EasyBooker"
class AgentFlowService:
    def __init__(self):
        self.stt_runner = InMemoryRunner(agent=stt_agent, app_name=APP_NAME)
        self.npl_runner = InMemoryRunner(agent=npl_agent, app_name=APP_NAME)
        self.suggestor_runner = InMemoryRunner(agent=suggestor_agent, app_name=APP_NAME)
        self.scheduler_runner = InMemoryRunner(agent=scheduler_agent, app_name=APP_NAME)
        self.normalizer_runner = InMemoryRunner(agent=normalizer_agent, app_name=APP_NAME)

    async def execute_stt(
        self, prompt: str, user_id: str, session: str
    ) -> tuple[str, Exception]:
        print("🎤 [1/3] Transcrevendo áudio...")
        content_stt = Content(role="user", parts=[Part(text=prompt)])
        session_id = f"{session}_stt"

        await self.stt_runner.session_service.create_session(
            app_name=APP_NAME, user_id=user_id, session_id=session_id
        )

        texto_transcrito = None
        async for event in self.stt_runner.run_async(
            user_id=user_id, session_id=session_id, new_message=content_stt
        ):
            if hasattr(event, "content") and event.content and event.content.parts:
                for parte in event.content.parts:
                    if hasattr(parte, "text") and parte.text:
                        texto_transcrito = parte.text

        if not texto_transcrito:
            return None, Exception("Falha na transcrição do áudio")

        print(f"Texto transcrito: {texto_transcrito}")
        return texto_transcrito, None


    async def execute_npl(
        self, prompt: str, user_id: str, session: str
    ) -> tuple[str, Exception]:
        print("🤖 [2/3] Processando texto...")
        content_npl = Content(role="user", parts=[Part(text=prompt)])
        evento_json = None
        session_id = f"{session}_npl"

        await self.npl_runner.session_service.create_session(
            app_name=APP_NAME, user_id=user_id, session_id=session_id
        )

        async for event in self.npl_runner.run_async(
            user_id=user_id, session_id=session_id, new_message=content_npl
        ):
            if hasattr(event, "content") and event.content and event.content.parts:
                for parte in event.content.parts:
                    if hasattr(parte, "text") and parte.text:
                        evento_json = parte.text

        if not evento_json:
            return None, Exception("Falha na extração de dados")

        print(f"Evento estruturado: {evento_json}")
        return evento_json, None


    async def execute_suggestor(
        self, prompt: str, user_id: str, session: str
    ) -> tuple[str, Exception]:
        print("💡 [3/3] Criando sugestão...")
        content_suggestor = Content(role="user", parts=[Part(text=prompt)])
        session_id = f"{session}_suggestor"

        await self.suggestor_runner.session_service.create_session(
            app_name=APP_NAME, user_id=user_id, session_id=session_id
        )

        async for event in self.suggestor_runner.run_async(
            user_id=user_id, session_id=session_id, new_message=content_suggestor
        ):
            if hasattr(event, "content") and event.content and event.content.parts:
                for parte in event.content.parts:
                    if hasattr(parte, "text") and parte.text:
                        sugestao = parte.text

        if not sugestao:
            return None, Exception("Falha na criação da sugestão")

        print(f"Sugestão: {sugestao}")
        try:
            response_obj = json.loads(sugestao)
            response_inline = json.dumps(
                response_obj, ensure_ascii=False, separators=(",", ":")
            )
            return response_inline, None
        except json.JSONDecodeError:
            return sugestao, None


    async def execute_scheduler(
        self, prompt: str, user_id: str, session: str
    ) -> tuple[str, Exception]:
        print("🕒 [4/4] Agendando compromisso...")
        content_scheduler = Content(role="user", parts=[Part(text=prompt)])
        session_id = f"{session}_scheduler"

        await self.scheduler_runner.session_service.create_session(
            app_name=APP_NAME, user_id=user_id, session_id=session_id
        )

        async for event in self.scheduler_runner.run_async(
            user_id=user_id, session_id=session_id, new_message=content_scheduler
        ):
            if hasattr(event, "content") and event.content and event.content.parts:
                for parte in event.content.parts:
                    if hasattr(parte, "text") and parte.text:
                        response = parte.text

        if not response:
            return None, Exception("Falha no agendamento")

        print(f"Agendamento: {response}, user_id: {user_id}")
        return response, None

    async def execute_normalizer(
        self, prompt: str, user_id: str, session: str
    ) -> tuple[str, Exception]:
        print("🔍 [5/5] Normalizando resposta...")
        content_normalizer = Content(role="user", parts=[Part(text=prompt)])
        session_id = f"{session}_normalizer"

        await self.normalizer_runner.session_service.create_session(
            app_name=APP_NAME, user_id=user_id, session_id=session_id
        )

        async for event in self.normalizer_runner.run_async(
            user_id=user_id, session_id=session_id, new_message=content_normalizer
        ):
            if hasattr(event, "content") and event.content and event.content.parts:
                for parte in event.content.parts:
                    if hasattr(parte, "text") and parte.text:
                        response = parte.text

        if not response:
            return None, Exception("Falha na normalização da resposta")

        print(f"Resposta normalizada: {response}")
        return response, None