import importlib
import time
from dotenv import load_dotenv
from loguru import logger
from app.models.dataclass import Log, LogLevel  # Certifique-se de que o caminho está correto

load_dotenv()


class Logs:
    """
    Classe para gerenciamento de logs com integração com Loguru e MongoDB.
    """

    def __init__(self):
        pass  # O __init__ fica vazio

    @staticmethod
    def return_log(name, cron_id=None, session_id=None):
        """
        Retorna uma instância de log configurada, incluindo cron_id e session_id se fornecidos.
        Faz a configuração do logger e testa a conexão com o MongoDB.
        """
        Database = importlib.import_module("app.core.db.mongo").Database  # Ajuste o caminho para o módulo correto

        # Configura o MongoDB e testa a conexão uma vez
        db = Database()

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
        return logger.bind(name=name, cron_id=cron_id, session_id=session_id)

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
                    cron_id=message.record["extra"].get("cron_id"),
                    session_id=message.record["extra"].get("session_id"),
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