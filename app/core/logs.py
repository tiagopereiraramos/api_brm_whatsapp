from dataclasses import asdict, dataclass, field
from datetime import datetime
from enum import Enum
import time
from typing import Any, Dict, Optional

from pydantic import BaseModel
from loguru import logger
from app.core.mongo import AsyncDatabase


# ---------- ENUMS ----------
class LogLevel(Enum):
    INFO = "INFO"
    ERROR = "ERROR"
    WARNING = "WARNING"
    DEBUG = "DEBUG"
    CRITICAL = "CRITICAL"

# Log dataclass


class Log(BaseModel):
    _id: Optional[str] = field(default=None, init=False)
    level: Optional[LogLevel] = None
    time: Optional[datetime] = None
    message: Optional[str] = None

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Log":
        try:
            return Log(
                level=LogLevel(data["level"]) if data.get("level") else None,
                time=(
                    datetime.fromisoformat(
                        data["time"]) if data.get("time") else None
                ),
                message=data.get("message"),
            )
        except Exception as e:
            print(f"Erro ao converter dicionário para Log: {e}")
            return None

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)  # Converte a dataclass para um dicionário
        data = {
            k: v for k, v in data.items() if v is not None
        }  # Remove os valores None

        # Converte o nível (LogLevel) para string, se necessário
        if "level" in data and isinstance(data["level"], Enum):
            data["level"] = data["level"].value

        # Converte o tempo (datetime) para ISO 8601, se necessário
        if "time" in data and isinstance(data["time"], datetime):
            data["time"] = data["time"].isoformat()

        return data


class Logs:
    """
    Classe para gerenciamento de logs com integração com Loguru e MongoDB.
    """

    def __init__(self):
        pass  # O __init__ fica vazio

    @staticmethod
    def return_log(name):
        """
        Retorna uma instância de log configurada, incluindo cron_id e session_id se fornecidos.
        Faz a configuração do logger e testa a conexão com o MongoDB.
        """
        # Ajuste o caminho para o módulo correto

        # Configura o MongoDB e testa a conexão uma vez
        db = AsyncDatabase()

        # Remove handlers padrões para evitar duplicação
        logger.remove()
        log_format = "<green>{time}</green> - <level>{level}</level>: <cyan>{name}</cyan> - <level>{message}</level>"

        # Adiciona um único handler que grava no console e no MongoDB, dependendo do nível
        logger.add(
            Logs.log_handler(db),
            format=log_format,
            level="DEBUG",
            colorize=True,
        )

        # Retorna o logger configurado com os valores bindados (cron_id e session_id)
        return logger.bind(name=name)

    @staticmethod
    def log_handler(db):
        """
        Handler para processar logs e gravar no MongoDB conforme o nível.
        """
        def handler(message):
            print(message, end="")  # Log para o console

            # Grava no MongoDB apenas se o nível for INFO ou superior
            if message.record["level"].no >= logger.level("INFO").no:
                log = Log(

                    level=LogLevel(
                        message.record["level"].name
                    ),  # Garantir que seja enum
                    time=message.record["time"],
                    message=message.record["message"],
                )

                try:
                    db.log.create(log)  # Passa a instância diretamente
                except Exception as e:
                    print(f"Falha ao enviar log para MongoDB: {e}")

        return handler


# Decorador para rastrear o início e fim dos processos
def log_process(func):
    """
    Decorador para registrar o início, fim e exceções de um processo, contabilizando o tempo de execução.
    """

    def wrapper(*args, **kwargs):
        # Cria uma instância de logger para a função decorada
        log = Logs.return_log(func.__name__)

        start_time = time.time()  # Início do tempo
        log.info(f"Starting {func.__name__}")

        try:
            result = func(*args, **kwargs)
            duration = time.time() - start_time  # Calcula o tempo decorrido
            log.info(
                f"Process completed successfully in {duration:.2f} seconds."
            )
            return result
        except Exception as e:
            duration = time.time() - start_time  # Calcula o tempo até a falha
            log.error(
                f"Process failed after {duration:.2f} seconds with error: {e}"
            )
            raise
        finally:
            log.info(f"Ending {func.__name__}")

    return wrapper
