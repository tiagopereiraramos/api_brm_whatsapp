from db.mongo import Database
from app.models.template import TemplateCobranca
from typing import List, Optional


class TemplateService:
    db = Database()

    @staticmethod
    def create_template(template: TemplateCobranca) -> str:
        return TemplateService.db.template_cobranca.create(template)

    @staticmethod
    def list_templates(empresa_id: str) -> List[TemplateCobranca]:
        return TemplateService.db.template_cobranca.read({"empresa_id": empresa_id})

    @staticmethod
    def get_template_by_id(id: str) -> Optional[TemplateCobranca]:
        return TemplateService.db.template_cobranca.read({"_id": id})

    @staticmethod
    def delete_template(id: str) -> int:
        return TemplateService.db.template_cobranca.delete({"_id": id})

    @staticmethod
    def update_template(id: str, update_data: dict) -> Optional[str]:
        return TemplateService.db.template_cobranca.update({"_id": id}, update_data)