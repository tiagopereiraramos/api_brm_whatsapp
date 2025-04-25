from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime
from enum import Enum


# Enum para StatusEmpresa
class StatusEmpresa(Enum):
    ATIVA = "ativa"
    INATIVA = "inativa"
    SUSPENSA = "suspensa"


# Classe Empresa usando dataclass
@dataclass
class Empresa:
    _id: Optional[str] = None
    nome: str = ""
    cnpj: Optional[str] = None
    status: StatusEmpresa = StatusEmpresa.ATIVA.value
    hash_autenticacao: str = ""
    valor_mensalidade: float = 0.0
    data_inicio_contrato: datetime = field(default_factory=datetime.now)
    data_fim_contrato: Optional[datetime] = None
    ciclo_pagamento: Optional[str] = "mensal"
    observacoes: Optional[str] = None
