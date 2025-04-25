from temporalio import workflow, activity
from typing import Dict
from datetime import datetime
import requests
from app.services.evolution_service import EvolutionService
from app.models.mensagem.mensagem import StatusEnvio
from app.config.config import getenv

# Configuração do EvolutionService
evolution_service = EvolutionService(
    base_url=getenv("EVOLUTION_BASE_URL"),
    apikey=getenv("EVOLUTION_API_KEY"),
    instance=getenv("EVOLUTION_API_INSTANCE"),
)

# Activity para enviar a mensagem


@activity.defn
async def send_message_activity(numero_destino: str, texto: str) -> Dict:
    """
    Activity que envia a mensagem usando o EvolutionService.
    """
    try:
        response = evolution_service.send_text_message(
            number=numero_destino,
            text=texto
        )
        return response
    except requests.ConnectionError as conn_error:
        raise RuntimeError(f"Erro de conexão: {conn_error}")
    except requests.Timeout as timeout_error:
        raise RuntimeError(f"Timeout: {timeout_error}")
    except requests.RequestException as req_error:
        raise RuntimeError(f"Erro na requisição: {req_error}")

# Workflow para orquestrar o envio da mensagem


@workflow.defn
class SendMessageWorkflow:
    @workflow.run
    async def run(self, numero_destino: str, texto: str) -> Dict:
        """
        Workflow que orquestra o envio da mensagem.
        """
        result = await workflow.execute_activity(
            send_message_activity,
            numero_destino,
            texto,
            schedule_to_close_timeout=datetime.timedelta(seconds=30),
        )
        return result
