from fastapi import APIRouter, HTTPException
from datetime import datetime
from uuid import uuid4
import requests
from app.config.config import getenv
from app.models.mensagem.mensagem_request import MensagemRequest
from app.models.mensagem.mensagem_response import MensagemResponse
from app.services.evolution_service import EvolutionService
from app.models.mensagem.mensagem import StatusEnvio
from app.core.logs import Logs
from app.tasks.enviar_mensagem_task import enviar_mensagem_task


logger = Logs.return_log(__name__)

# Cria o roteador para os endpoints de mensagem
router = APIRouter()


@router.post("/mensagens/enviar", response_model=MensagemResponse)
async def enviar_mensagem(mensagem_request: MensagemRequest):
    # Gera ID, formata texto, valida...
    texto = mensagem_request.template.format(**mensagem_request.payload)

    # Chama a task no background
    enviar_mensagem_task.delay(mensagem_request.numero_destino, texto)

    return MensagemResponse(
        _id=str(uuid4()),
        empresa_id=mensagem_request.empresa_id,
        numero_destino=mensagem_request.numero_destino,
        template=mensagem_request.template,
        payload=mensagem_request.payload,
        status_envio=StatusEnvio.PENDENTE,
        tentativas=0,
        data_envio=datetime.utcnow()
    )
