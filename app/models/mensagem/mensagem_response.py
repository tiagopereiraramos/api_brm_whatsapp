from pydantic import BaseModel
from datetime import datetime
from enum import Enum
from typing import Dict, Optional

# Enum para status de envio de mensagem
class StatusEnvio(str, Enum):
    SUCESSO = "sucesso"
    ERRO = "erro"
    PENDENTE = "pendente"

class MensagemResponse(BaseModel):
    """
    Modelo Pydantic para representar a resposta do envio de mensagem.
    """
    _id: str
    empresa_id: str
    numero_destino: str
    template: str
    payload: Dict[str, str]
    status_envio: StatusEnvio
    tentativas: int
    data_envio: Optional[datetime]

    class Config:
        schema_extra = {
            "example": {
                "_id": "abc123",
                "empresa_id": "123456",
                "numero_destino": "5567999087301",
                "template": "Olá, {nome}! Sua entrega está a caminho.",
                "payload": {
                    "nome": "João"
                },
                "status_envio": "sucesso",
                "tentativas": 1,
                "data_envio": "2025-04-24T02:00:05"
            }
        }