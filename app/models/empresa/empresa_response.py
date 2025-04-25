from pydantic import BaseModel
from datetime import datetime
from enum import Enum
from typing import Optional

# Enum para status da empresa


class StatusEmpresa(str, Enum):
    ATIVA = "ativa"
    INATIVA = "inativa"
    SUSPENSA = "suspensa"


class EmpresaResponse(BaseModel):
    """
    Modelo Pydantic para representar a resposta de uma empresa.
    """
    _id: str
    nome: str
    cnpj: Optional[str]
    status: StatusEmpresa
    hash_autenticacao: str  # Campo para o hash de autenticação da empresa
    valor_mensalidade: float
    data_inicio_contrato: datetime
    data_fim_contrato: Optional[datetime]
    ciclo_pagamento: Optional[str]
    observacoes: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "_id": "1234567890abcdef",
                "nome": "Empresa Exemplo LTDA",
                "cnpj": "12345678000195",
                "status": "ativa",
                "hash_autenticacao": "abc123def456",
                "valor_mensalidade": 500.00,
                "data_inicio_contrato": "2025-01-01T00:00:00",
                "data_fim_contrato": "2026-01-01T00:00:00",
                "ciclo_pagamento": "mensal",
                "observacoes": "Cliente em dia com pagamentos"
            }
        }
