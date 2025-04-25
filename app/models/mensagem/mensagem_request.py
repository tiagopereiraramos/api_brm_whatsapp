from pydantic import BaseModel, Field
from typing import Dict

class MensagemRequest(BaseModel):
    """
    Modelo Pydantic para representar a requisição de envio de mensagem.
    """
    empresa_id: str = Field(..., example="123456")
    numero_destino: str = Field(..., example="5567999087301", description="Número do destinatário no formato internacional")
    template: str = Field(..., example="Olá, {nome}! Sua entrega está a caminho.")
    payload: Dict[str, str] = Field(..., example={"nome": "João"})

    class Config:
        schema_extra = {
            "example": {
                "empresa_id": "123456",
                "numero_destino": "5567999087301",
                "template": "Olá, {nome}! Sua entrega está a caminho.",
                "payload": {
                    "nome": "João"
                }
            }
        }