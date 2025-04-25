from fastapi import APIRouter, HTTPException
from app.models.empresa.empresa_request import EmpresaRequest
from app.models.empresa.empresa_response import EmpresaResponse
from app.models.empresa.empresa import Empresa  # Dataclass Empresa
from app.core.mongo import AsyncDatabase  # Classe AsyncDatabase
from dataclasses import asdict
from bson import ObjectId, errors
from typing import List

# Inicializa o roteador e o banco de dados
router = APIRouter()
db = AsyncDatabase()


@router.post("/", response_model=EmpresaResponse)
async def create_empresa(request: EmpresaRequest) -> EmpresaResponse:
    """
    Cria uma nova empresa no banco de dados.
    """
    # Converte o Pydantic request para um dataclass Empresa
    empresa = Empresa(
        _id=None,  # MongoDB irá gerar o _id automaticamente
        nome=request.nome,
        cnpj=request.cnpj,
        status=request.status,
        hash_autenticacao=request.hash_autenticacao,
        valor_mensalidade=request.valor_mensalidade,
        data_inicio_contrato=request.data_inicio_contrato,
        data_fim_contrato=request.data_fim_contrato,
        ciclo_pagamento=request.ciclo_pagamento,
        observacoes=request.observacoes,
    )

    # Insere no banco de dados usando o método create
    try:
        inserted_id = await db.empresa.create(empresa)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erro ao criar empresa: {str(e)}")

    # Retorna a resposta no formato EmpresaResponse
    empresa_response = EmpresaResponse(
        _id=inserted_id,
        nome=empresa.nome,
        cnpj=empresa.cnpj,
        status=empresa.status,
        hash_autenticacao=empresa.hash_autenticacao,
        valor_mensalidade=empresa.valor_mensalidade,
        data_inicio_contrato=empresa.data_inicio_contrato,
        data_fim_contrato=empresa.data_fim_contrato,
        ciclo_pagamento=empresa.ciclo_pagamento,
        observacoes=empresa.observacoes,
    )
    return empresa_response


@router.get("/", response_model=List[EmpresaResponse])
async def get_empresas() -> List[EmpresaResponse]:
    """
    Recupera todas as empresas do banco de dados.
    """
    try:
        empresas = await db.empresa.read_all()
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erro ao buscar empresas: {str(e)}")

    # Converte os resultados do dataclass Empresa para EmpresaResponse
    return [
        EmpresaResponse(
            _id=str(empresa._id),
            nome=empresa.nome,
            cnpj=empresa.cnpj,
            status=empresa.status,
            hash_autenticacao=empresa.hash_autenticacao,
            valor_mensalidade=empresa.valor_mensalidade,
            data_inicio_contrato=empresa.data_inicio_contrato,
            data_fim_contrato=empresa.data_fim_contrato,
            ciclo_pagamento=empresa.ciclo_pagamento,
            observacoes=empresa.observacoes,
        )
        for empresa in empresas
    ]


@router.get("/{empresa_id}", response_model=EmpresaResponse)
async def get_empresa(empresa_id: str) -> EmpresaResponse:
    """
    Recupera uma empresa específica pelo ID.
    """
    try:
        # Valida o ID antes de buscar
        if not ObjectId.is_valid(empresa_id):
            raise HTTPException(
                status_code=400, detail="ID de empresa inválido.")

        empresa = await db.empresa.read({"_id": ObjectId(empresa_id)})
        if not empresa:
            raise HTTPException(
                status_code=404, detail="Empresa não encontrada.")
    except errors.InvalidId:
        raise HTTPException(status_code=400, detail="Formato de ID inválido.")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erro ao buscar empresa: {str(e)}")

    return EmpresaResponse(
        _id=str(empresa._id),
        nome=empresa.nome,
        cnpj=empresa.cnpj,
        status=empresa.status,
        hash_autenticacao=empresa.hash_autenticacao,
        valor_mensalidade=empresa.valor_mensalidade,
        data_inicio_contrato=empresa.data_inicio_contrato,
        data_fim_contrato=empresa.data_fim_contrato,
        ciclo_pagamento=empresa.ciclo_pagamento,
        observacoes=empresa.observacoes,
    )


@router.put("/{empresa_id}", response_model=EmpresaResponse)
async def update_empresa(empresa_id: str, request: EmpresaRequest) -> EmpresaResponse:
    """
    Atualiza uma empresa existente no banco de dados.
    """
    # Converte o Pydantic request para um dicionário
    update_data = asdict(
        Empresa(
            _id=None,  # Não alteramos o _id no update
            nome=request.nome,
            cnpj=request.cnpj,
            status=request.status,
            hash_autenticacao=request.hash_autenticacao,
            valor_mensalidade=request.valor_mensalidade,
            data_inicio_contrato=request.data_inicio_contrato,
            data_fim_contrato=request.data_fim_contrato,
            ciclo_pagamento=request.ciclo_pagamento,
            observacoes=request.observacoes,
        )
    )
    # Remove o _id do dicionário, pois não será atualizado
    update_data.pop("_id", None)

    try:
        # Valida o ID antes de atualizar
        if not ObjectId.is_valid(empresa_id):
            raise HTTPException(
                status_code=400, detail="ID de empresa inválido.")

        updated_id = await db.empresa.update({"_id": ObjectId(empresa_id)}, update_data)
        if not updated_id:
            raise HTTPException(
                status_code=404, detail="Empresa não encontrada para atualização.")
    except errors.InvalidId:
        raise HTTPException(status_code=400, detail="Formato de ID inválido.")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erro ao atualizar empresa: {str(e)}")

    return EmpresaResponse(
        _id=empresa_id,
        nome=request.nome,
        cnpj=request.cnpj,
        status=request.status,
        hash_autenticacao=request.hash_autenticacao,
        valor_mensalidade=request.valor_mensalidade,
        data_inicio_contrato=request.data_inicio_contrato,
        data_fim_contrato=request.data_fim_contrato,
        ciclo_pagamento=request.ciclo_pagamento,
        observacoes=request.observacoes,
    )


@router.delete("/{empresa_id}", response_model=dict)
async def delete_empresa(empresa_id: str) -> dict:
    """
    Deleta uma empresa específica pelo ID.
    """
    try:
        # Valida o ID antes de deletar
        if not ObjectId.is_valid(empresa_id):
            raise HTTPException(
                status_code=400, detail="ID de empresa inválido.")

        deleted_count = await db.empresa.delete({"_id": ObjectId(empresa_id)})
        if deleted_count == 0:
            raise HTTPException(
                status_code=404, detail="Empresa não encontrada para exclusão.")
    except errors.InvalidId:
        raise HTTPException(status_code=400, detail="Formato de ID inválido.")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erro ao deletar empresa: {str(e)}")

    return {"message": "Empresa deletada com sucesso"}
