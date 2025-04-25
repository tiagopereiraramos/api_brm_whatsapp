from pydantic_settings import BaseSettings
from pydantic import Field
from typing import List, Optional
import os


class Settings(BaseSettings):
    # Ambiente
    env: str = Field(..., env="ENV")
    local_mongo_database_dev: str = Field(..., env="LOCAL_MONGO_DATABASE_DEV")
    local_mongo_database_prod: str = Field(...,
                                           env="LOCAL_MONGO_DATABASE_PROD")

    # Mapeamento de coleções para dataclasses
    collections: str = Field(..., env="COLLECTIONS")

    # Configuração MongoDB
    mongo_uri: str = Field(..., env="MONGO_URI")

    # Configuração MinIO
    bucket_name: str = Field(..., env="BUCKET_NAME")
    minio_access_key: str = Field(..., env="MINIO_ACCESS_KEY")
    minio_endpoint: str = Field(..., env="MINIO_ENDPOINT")
    minio_secret_key: str = Field(..., env="MINIO_SECRET_KEY")

    # Configuração Evolution
    evolution_base_url: str = Field(..., env="EVOLUTION_BASE_URL")
    evolution_api_key: str = Field(..., env="EVOLUTION_API_KEY")
    evolution_api_instance: str = Field(..., env="EVOLUTION_API_INSTANCE")

    # Configuração Coda API
    coda_api_base_url: str = Field(..., env="CODA_API_BASE_URL")
    coda_api_token: str = Field(..., env="CODA_API_TOKEN")
    coda_document_id: str = Field(..., env="CODA_DOCUMENT_ID")

    # Configuração Celery
    celery_broker_url: str = Field(..., env="CELERY_BROKER_URL")
    celery_result_backend: str = Field(..., env="CELERY_RESULT_BACKEND")

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
    }


settings = Settings()


def getenv(key: str, default: Optional[str] = None) -> Optional[str]:
    """
    Função auxiliar para manter compatibilidade com o legado.
    Busca a chave no Pydantic Settings primeiro, depois tenta no os.environ.
    """
    normalized_key = key.lower().strip()

    # Busca direto em Settings usando __dict__ para debug e flexibilidade
    value = getattr(settings, normalized_key, None)
    if value is not None:
        print(
            f"[Settings] {key} = {value if 'key' not in key.lower() else '***'}"
        )
        return value

    # Fallback para os.environ, com debug
    fallback = os.getenv(key, default)
    print(
        f"[os.environ] {key} = {fallback if 'key' not in key.lower() else '***'}"
    )
    return fallback
