from dataclasses import dataclass
from enum import Enum
from typing import Optional

# Enum para tipo de WhatsApp
class TipoWhatsapp(str, Enum):
    OFICIAL = "oficial"
    EVOLUTION = "evolution"

@dataclass
class ConfiguracaoWhatsapp:
    _id: Optional[str]
    empresa_id: str
    tipo: TipoWhatsapp
    token: str
    remetente_padrao: str