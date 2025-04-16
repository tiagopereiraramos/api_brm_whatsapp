import os
from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Ambiente
    env: str
    mode: str
    mongo_uri: str
    local_mongo_database_dev: str
    local_mongo_database_prod: str
    collections: str
    mode: str = "debug"
    # Planilha de dados
    dados_acesso: str = ""

    script_path: Optional[str] = ""
    python_path: Optional[str] = ""
    # Dados de acesso SAT
    login: str
    senha: str
    urlsat: str

    # MinIO
    minio_endpoint: str
    minio_access_key: str
    minio_secret_key: str
    bucket_name: str

    # Coda
    coda_api_base_url: str
    coda_api_token: str
    coda_document_id: str

    credentials_google: str
    token_google: str
    rabbitmq_url: str
    scopes:str

    class Config:
        env_file = ".env"  # Configura o caminho para o arquivo .env


# Criar uma instância única (singleton) para ser usada em todo o projeto
settings = Settings()


# Função compatível com os.getenv
def getenv(key: str, default=None):
    # Primeiro, tenta pegar a variável do Pydantic (settings)
    try:
        return getattr(settings, key, os.getenv(key, default))
    except AttributeError:
        return getenv(key, default)
