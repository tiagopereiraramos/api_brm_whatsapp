from db.mongo import Database
from app.models.whatsapp import ConfiguracaoWhatsapp
from typing import Optional


class WhatsappService:
    db = Database()

    @staticmethod
    def save_config(config: ConfiguracaoWhatsapp) -> str:
        return WhatsappService.db.configuracao_whatsapp.create(config)

    @staticmethod
    def get_config_by_empresa(empresa_id: str) -> Optional[ConfiguracaoWhatsapp]:
        return WhatsappService.db.configuracao_whatsapp.read({"empresa_id": empresa_id})

    @staticmethod
    def update_config(empresa_id: str, update_data: dict) -> Optional[str]:
        return WhatsappService.db.configuracao_whatsapp.update({"empresa_id": empresa_id}, update_data)