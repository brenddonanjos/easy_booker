from datetime import datetime
from zoneinfo import ZoneInfo
from fastapi import APIRouter, File, UploadFile
import json
import os
import uuid
from fastapi.responses import JSONResponse

from api.agent_flow_service import AgentFlowService
from api.dto import ResponseScheduleDTO


class AgentFlowController:
    def __init__(self, service: AgentFlowService):
        self.service = service

    async def schedule(
        self, user_id: str, file: UploadFile = File(...)
    ) -> tuple[ResponseScheduleDTO, None] | tuple[None, BaseException]:
        temp_audio_path = None
        try:
            unique_id = str(uuid.uuid4())[:8]
            file_extension = (
                os.path.splitext(file.filename)[1] if file.filename else ".mp3"
            )
            temp_audio_name = f"temp_{unique_id}{file_extension}"
            temp_audio_path = f"agents/stt_agent/{temp_audio_name}"
            session = f"session_{unique_id}"

            content = await file.read()
            with open(temp_audio_path, "wb") as f:
                f.write(content)

            prompt = f"Transcreva o áudio {temp_audio_name} para texto"

            response_stt, err = await self.service.execute_stt(
                prompt=prompt, user_id=user_id, session=session
            )
            if err:
                raise Exception(f"Erro na transcrição do áudio: {err}")

            now = datetime.now(ZoneInfo("America/Sao_Paulo"))
            response_stt = f"Data atual: {now.strftime('%d/%m/%Y')}\nhorário atual: {now.strftime('%H:%M')}\n Texto transcrito: {response_stt}"
            response_npl, err = await self.service.execute_npl(
                prompt=response_stt, user_id=user_id, session=session
            )
            if err:
                raise Exception(f"Erro na conversão do texto para objeto json: {err}")

            response_suggestor, err = await self.service.execute_suggestor(
                prompt=response_npl, user_id=user_id, session=session
            )
            if err:
                raise Exception(f"Erro na criação da sugestão: {err}")

            prompt_scheduler = f"user_id: {user_id}\n{response_suggestor}"  # Adicionando o user_id ao prompt para o scheduler
            response_scheduler, err = await self.service.execute_scheduler(
                prompt=prompt_scheduler, user_id=user_id, session=session
            )
            if err:
                raise Exception(f"Erro no agendamento: {err}")

            response_normalizer, err = await self.service.execute_normalizer(
                prompt=response_scheduler, user_id=user_id, session=session
            )
            if err:
                raise Exception(f"Erro na normalização da resposta: {err}")

            try:
                response_object = json.loads(response_normalizer)
                success = response_object.get("success", False)
                if not success:
                    raise Exception(
                        f"Erro no agendamento: {response_object.get('message', 'Erro desconhecido')}"
                    )

                return (
                    ResponseScheduleDTO(
                        success=success,
                        message=response_object.get("message", ""),
                        link=response_object.get("link", None),
                    ),
                    None,
                )
            except json.JSONDecodeError:
                raise Exception(f"Resposta normalizada inválida: {response_normalizer}")

        except Exception as e:
            return None, str(e)
        finally:
            if temp_audio_path:
                os.remove(temp_audio_path)


def agent_flow_router(controller: AgentFlowController) -> APIRouter:
    router = APIRouter(prefix="/agents", tags=["Agent Flow"])

    @router.post("/schedule/{user_id}", response_model=ResponseScheduleDTO)
    async def schedule(user_id: str, file: UploadFile = File(...)):
        event, error = await controller.schedule(user_id, file)
        if error:
            response_error = ResponseScheduleDTO(
                success=False,
                message=str(error),
                link=None,
            )
            return JSONResponse(
                status_code=500,
                content=response_error.model_dump(), 
            )

        return event

    return router
