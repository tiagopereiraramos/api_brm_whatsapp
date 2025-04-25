import os
from typing import Optional, Any
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Ambiente
    env: str
    mode: str = "debug"

    # Banco de Dados MongoDB
    mongo_uri: str
    local_mongo_database_dev: str
    local_mongo_database_prod: str
    collections: str

    # Configuração MinIO
    minio_access_key: str
    minio_secret_key: str
    bucket_name: str
    minio_endpoint: str

    # Configuração Evolution
    evolution_base_url: str
    evolution_api_key: str
    evolution_api_instance: str

    # Configuração Coda API
    coda_api_base_url: str
    coda_api_token: str
    coda_document_id: str

    # Configuração do temporal.io
    celery_broker_url: str
    celery_result_backend: str
    # Credenciais do Google
    credentials_google: Optional[str] = None
    token_google: Optional[str] = None

    # Scopes do Google
    scopes: str

    class Config:
        env_file = ".env"


# Instância única (singleton) para ser usada em todo o projeto
settings = Settings()


def getenv(key: str, default: Any = None) -> Any:
    """
    Recupera o valor de uma variável de ambiente ou do arquivo .env.

    :param key: Nome da variável de ambiente.
    :param default: Valor padrão caso a variável não esteja definida.
    :return: Valor da variável de ambiente ou valor padrão.
    """
    normalized_key = key.lower()  # Converte para minúsculas
    print(f"Buscando chave normalizada: {normalized_key}")  # Debug

    # Primeiro tenta pegar do objeto `settings` (carregado pelo Pydantic)
    if hasattr(settings, normalized_key):
        value = getattr(settings, normalized_key)
        print(f"Valor encontrado em settings: {value}")  # Debug
        if value is not None and value != "":
            return value

    # Em seguida tenta pegar da variável de ambiente diretamente
    env_value = os.getenv(key, default)
    print(f"Valor encontrado em os.getenv: {env_value}")  # Debug
    return env_value
