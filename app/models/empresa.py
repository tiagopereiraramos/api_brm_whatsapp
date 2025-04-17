from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional

# Enum para status da empresa
class StatusEmpresa(str, Enum):
    ATIVO = "ativo"
    INATIVO = "inativo"

@dataclass
class Empresa:
    _id: Optional[str]
    nome: str
    status: StatusEmpresa
    hash_autenticacao: str
    valor_mensalidade: float
    data_inicio_contrato: datetime
    data_fim_contrato: Optional[datetime] = None
    ciclo_pagamento: Optional[str] = "mensal"
    observacoes: Optional[str] = None