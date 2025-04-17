from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional, Dict

# Enum para status de envio de mensagem
class StatusEnvio(str, Enum):
    SUCESSO = "sucesso"
    ERRO = "erro"
    PENDENTE = "pendente"

@dataclass
class Mensagem:
    _id: Optional[str]
    empresa_id: str
    numero_destino: str
    template: str
    payload: Dict[str, str]
    status_envio: StatusEnvio
    tentativas: int
    data_envio: Optional[datetime] = None