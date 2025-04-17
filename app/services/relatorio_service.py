from db.mongo import Database
from app.models.relatorio import RelatorioMensal
from typing import List, Optional


class RelatorioService:
    db = Database()

    @staticmethod
    def create_relatorio(relatorio: RelatorioMensal) -> str:
        return RelatorioService.db.relatorio_mensal.create(relatorio)

    @staticmethod
    def list_relatórios(empresa_id: str) -> List[RelatorioMensal]:
        return RelatorioService.db.relatorio_mensal.read({"empresa_id": empresa_id})

    @staticmethod
    def get_relatorio(empresa_id: str, mes_ano: str) -> Optional[RelatorioMensal]:
        return RelatorioService.db.relatorio_mensal.read({"empresa_id": empresa_id, "mes_ano": mes_ano})

    @staticmethod
    def update_relatorio(relatorio_id: str, update_data: dict) -> Optional[str]:
        return RelatorioService.db.relatorio_mensal.update({"_id": relatorio_id}, update_data)