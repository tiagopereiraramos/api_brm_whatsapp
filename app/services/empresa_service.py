from db.mongo import Database
from app.models.empresa import Empresa
from typing import List, Optional


class EmpresaService:
    db = Database()

    @staticmethod
    def create_empresa(empresa: Empresa) -> str:
        return EmpresaService.db.empresa.create(empresa)

    @staticmethod
    def list_empresas() -> List[Empresa]:
        return EmpresaService.db.empresa.read({})

    @staticmethod
    def get_empresa_by_id(id: str) -> Optional[Empresa]:
        return EmpresaService.db.empresa.read({"_id": id})

    @staticmethod
    def update_empresa(id: str, update_data: dict) -> Optional[str]:
        return EmpresaService.db.empresa.update({"_id": id}, update_data)

    @staticmethod
    def delete_empresa(id: str) -> int:
        return EmpresaService.db.empresa.delete({"_id": id})