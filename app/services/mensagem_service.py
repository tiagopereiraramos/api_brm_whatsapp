from db.mongo import Database
from app.models.mensagem import Mensagem
from typing import List, Optional


class MensagemService:
    db = Database()

    @staticmethod
    def create_mensagem(mensagem: Mensagem) -> str:
        return MensagemService.db.mensagem.create(mensagem)

    @staticmethod
    def list_mensagens(empresa_id: str) -> List[Mensagem]:
        return MensagemService.db.mensagem.read({"empresa_id": empresa_id})

    @staticmethod
    def get_mensagem_by_id(id: str) -> Optional[Mensagem]:
        return MensagemService.db.mensagem.read({"_id": id})

    @staticmethod
    def update_status_mensagem(id: str, status: str) -> Optional[str]:
        return MensagemService.db.mensagem.update({"_id": id}, {"status_envio": status})

    @staticmethod
    def delete_mensagem(id: str) -> int:
        return MensagemService.db.mensagem.delete({"_id": id})