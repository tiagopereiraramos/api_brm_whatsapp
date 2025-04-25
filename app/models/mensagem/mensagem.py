from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional, Dict

class StatusEnvio(str, Enum):
    SUCESSO = "sucesso"
    ERRO = "erro"
    PENDENTE = "pendente"

@dataclass
class Mensagem:
    empresa_id: Optional[str] = field(default=None)
    numero_destino: Optional[str] = field(default=None)
    template: Optional[str] = field(default=None)
    payload: Dict[str, str] = field(default_factory=dict)
    status_envio: StatusEnvio = StatusEnvio.PENDENTE
    tentativas: int = 0
    data_envio: Optional[datetime] = field(default=None)
    _id: Optional[str] = field(default=None)  # 👈 Corrigido aqui!
