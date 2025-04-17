from fastapi import APIRouter
from app.models.relatorio import RelatorioMensal
from app.services.relatorio_service import RelatorioService

router = APIRouter()

@router.get("/{empresa_id}/{mes_ano}")
async def obter_relatorio(empresa_id: str, mes_ano: str):
    relatorio = RelatorioService.get_relatorio(empresa_id, mes_ano)
    if not relatorio:
        return {"message": "Relatório não encontrado"}
    return {"data": relatorio}