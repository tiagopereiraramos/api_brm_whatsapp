from fastapi import APIRouter, HTTPException
from app.models.empresa import Empresa, StatusEmpresa
from app.services.empresa_service import EmpresaService
from datetime import datetime

router = APIRouter()

@router.post("/")
async def create_empresa(empresa: Empresa):
    created_empresa = EmpresaService.create_empresa(empresa)
    return {"message": "Empresa criada com sucesso", "data": created_empresa}

@router.get("/")
async def list_empresas():
    empresas = EmpresaService.list_empresas()
    return {"data": empresas}

@router.put("/{id}")
async def update_empresa(id: str, empresa: dict):
    updated_empresa = EmpresaService.update_empresa(id, empresa)
    if not updated_empresa:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")
    return {"message": "Empresa atualizada com sucesso", "data": updated_empresa}

@router.delete("/{id}")
async def delete_empresa(id: str):
    success = EmpresaService.delete_empresa(id)
    if not success:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")
    return {"message": "Empresa deletada com sucesso"}