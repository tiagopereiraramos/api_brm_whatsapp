from fastapi import APIRouter, HTTPException
from app.models.template import TemplateCobranca
from app.models.mensagem import Mensagem, StatusEnvio
from app.services.cobranca_service import CobrancaService
from app.services.mensagem_service import MensagemService
from datetime import datetime

router = APIRouter()

@router.post("/enviar")
async def enviar_cobranca(template: TemplateCobranca):
    try:
        # Gera o texto de envio e cria a mensagem
        texto_envio = template.gerar_texto_envio()
        mensagem = Mensagem(
            _id=None,
            empresa_id="empresa_id_placeholder",  # Substituir pelo ID real
            numero_destino=template.num_resp_financ,
            template="cobranca",
            payload={"texto_envio": texto_envio},
            status_envio=StatusEnvio.PENDENTE,
            tentativas=0,
        )

        # Envia para a fila e salva no banco
        CobrancaService.send_cobranca_to_queue(mensagem)
        MensagemService.create_mensagem(mensagem)

        return {"message": "Cobrança enviada com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))