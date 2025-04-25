from pydantic import BaseModel, Field, field_validator, ValidationError
from typing import Optional
from datetime import datetime
from enum import Enum
from app.util.utils import generate_hash_token_empresa


class StatusEmpresa(str, Enum):
    """
    Enum para representar os possíveis status de uma empresa.
    """
    ATIVA = "ativa"
    INATIVA = "inativa"
    SUSPENSA = "suspensa"


class EmpresaRequest(BaseModel):
    """
    Modelo Pydantic para representar a requisição de criação ou atualização de uma empresa.
    """
    nome: str = Field(..., example="Empresa Exemplo LTDA",
                      description="Nome da empresa")
    cnpj: str = Field(None, example="12345678000195",
                      description="CNPJ da empresa")
    status: StatusEmpresa = Field(..., example="ativa",
                                  description="Status da empresa: ativa, inativa ou suspensa")
    hash_autenticacao: Optional[str] = None  # Será gerado automaticamente
    valor_mensalidade: float = Field(..., gt=0, example=500.00,
                                     description="Valor mensal da assinatura da empresa")
    data_inicio_contrato: datetime = Field(
        ..., example="2025-01-01T00:00:00", description="Data de início do contrato")
    data_fim_contrato: Optional[datetime] = Field(
        None, example="2026-01-01T00:00:00", description="Data de término do contrato")
    ciclo_pagamento: Optional[str] = Field(
        "mensal", example="mensal", description="Ciclo de pagamento (ex: mensal, anual)")
    observacoes: Optional[str] = Field(
        None, example="Cliente em dia com pagamentos", description="Observações adicionais sobre a empresa")

    @field_validator("data_fim_contrato")
    def validate_data_fim_contrato(cls, data_fim, info):
        """
        Valida que a data de fim do contrato, se fornecida, seja posterior à data de início do contrato.
        """
        data_inicio = info.data.get("data_inicio_contrato")
        if data_fim and data_inicio and data_fim <= data_inicio:
            raise ValueError(
                "A data de término do contrato deve ser posterior à data de início.")
        return data_fim

    @field_validator("hash_autenticacao", mode="before")
    def generate_hash_autenticacao(cls, value, info):
        """
        Gera o hash de autenticação usando os valores de nome e CNPJ.
        """
        nome = info.data.get("nome")
        cnpj = info.data.get("cnpj")
        if not nome:
            raise ValueError(
                "O campo 'nome' é obrigatório para gerar o hash de autenticação.")
        return generate_hash_token_empresa(nome=nome, cnpj=cnpj)

    class Config:
        schema_extra = {
            "example": {
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
