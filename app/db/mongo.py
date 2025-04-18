import hashlib
import importlib
import math
import uuid
from dataclasses import asdict
from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional, Type
from bson import ObjectId

from config.config import getenv
from pymongo import MongoClient
from util.dataclass import (
    Cadastro,
    Log,
    LogLevel,
    WebhookPayload,
)


class Database:
    """
    Classe principal para manipular o banco de dados MongoDB,
    incluindo configurações dinâmicas de coleções e
    operações relacionadas a processos, faturas e logs.
    """

    # ---------- Inicialização e Configuração ----------

    def __init__(self):
        """Inicializa a conexão com o MongoDB e configura as coleções."""
        self.env = getenv("ENV", "prod").lower()
        self.uri = getenv("MONGO_URI", "mongodb://localhost:27017")
        self.database_name = (
            getenv("LOCAL_MONGO_DATABASE_DEV")
            if self.env == "dev"
            else getenv("LOCAL_MONGO_DATABASE_PROD")
        )
        self.is_dev = self.env == "dev"
        self.collections = self.load_collections_from_env()

        # Conecta ao MongoDB
        self.client = MongoClient(self.uri)
        self.db = self.client[self.database_name]

        # Configura collections como atributos dinâmicos
        for collection_name, dataclass_type in self.collections.items():
            setattr(
                self,
                collection_name,
                self._create_collection_accessor(
                    collection_name, dataclass_type
                ),
            )

    def load_collections_from_env(self) -> Dict[str, Type]:
        """Carrega as coleções definidas na variável de ambiente COLLECTIONS."""
        collections_str = getenv("COLLECTIONS", "")
        collections = {}
        if collections_str:
            for item in collections_str.split(","):
                try:
                    collection_name, dataclass_name = item.split(":")
                    dataclass_module = importlib.import_module(
                        "util.dataclass"
                    )
                    dataclass_type = getattr(dataclass_module, dataclass_name)
                    collections[collection_name] = dataclass_type
                except (ValueError, ImportError, AttributeError) as e:
                    print(f"Erro ao carregar coleção: {item}. Detalhes: {e}")
        return collections

    # ---------- Auxiliares e Utilitários ----------

    def generate_hash_cad(self, nome_filtro: str, operadora: str, servico: str, dados_sat: str, filtro: str, unidade: str) -> str:
        """Gera um hash único para cada execução de um processo."""
        # Remover espaços nas variáveis e normalizar para minúsculas
        nome_filtro = nome_filtro.strip().lower()
        operadora = operadora.strip().lower()
        servico = servico.strip().lower()
        dados_sat = dados_sat.strip().lower()
        filtro = filtro.strip().lower()
        unidade = unidade.strip().lower()

        # Gerar a string base para o hash
        base_string = f"{nome_filtro}-{operadora}-{servico}-{dados_sat}-{filtro}-{unidade}"
        # Gerar o hash
        hash_value = hashlib.sha256(base_string.encode()).hexdigest()[:16]

        return hash_value

    def generate_session_id(self, hash_cad: str) -> str:
        """Gera um session_id único para cada execução de um processo."""
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        return hashlib.sha256(f"{hash_cad}-{timestamp}".encode()).hexdigest()[
            :16
        ]

    def generate_process_id(self, palavrachave: str = "TPSM") -> str:
        """Gera um identificador único para o processo."""
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        unique_id = uuid.uuid4().hex  # UUID aleatório
        random_salt = str(uuid.uuid4())[
            :8
        ]  # Pegamos uma parte do UUID como salt

        raw_string = f"{palavrachave}-{timestamp}-{unique_id}-{random_salt}"
        return hashlib.sha256(raw_string.encode()).hexdigest()[:16]

    # ---------- Acesso e Operações CRUD ----------

    def _create_collection_accessor(
        self, collection_name: str, dataclass_type: Type
    ):
        """Cria uma classe para acessar coleções no MongoDB com operações CRUD."""

        class CollectionAccessor:
            def __init__(self, db, collection_name, dataclass_type):
                self.collection = db[collection_name]
                self.dataclass_type = dataclass_type

            @staticmethod
            def mongo_to_python(value: Any) -> Any:
                """Converte valores do MongoDB para tipos Python compatíveis."""
                if isinstance(value, dict) and "$date" in value:
                    # Converte timestamp MongoDB para datetime
                    return datetime.strptime(
                        value["$date"], "%Y-%m-%dT%H:%M:%S.%fZ"
                    )
                elif isinstance(value, ObjectId):
                    return str(value)
                elif isinstance(value, list):
                    # Converte listas recursivamente
                    return [
                        CollectionAccessor.mongo_to_python(v) for v in value
                    ]
                elif isinstance(value, dict):
                    # Converte dicionários recursivamente
                    return {
                        k: CollectionAccessor.mongo_to_python(v)
                        for k, v in value.items()
                    }
                return value

            @staticmethod
            def clean_field(value: Any) -> Optional[Any]:
                """Valida e limpa campos, convertendo enums e ignorando valores inválidos."""
                if value is None or (
                    isinstance(value, float) and math.isnan(value)
                ):
                    return None
                # Converte enums para seus valores
                if isinstance(value, Enum):
                    return value.value
                if isinstance(value, str):
                    return value
                return value

            def create(self, obj: Any) -> str:
                if not isinstance(obj, self.dataclass_type):
                    raise TypeError(
                        f"Expected instance of {self.dataclass_type}, got {type(obj)}"
                    )

                document = asdict(obj)

                # Limpar todos os campos dinamicamente
                for key, value in document.items():
                    document[key] = self.clean_field(value)

                if "_id" in document and document["_id"] is None:
                    del document["_id"]

                result = self.collection.insert_one(document)
                return str(result.inserted_id)

            def read(self, query: Dict) -> Any:
                """
                Lê os documentos de acordo com a consulta fornecida e converte para instâncias do dataclass.
                O _id será incluído como opcional nas instâncias.
                """
                documents = self.collection.find(query)
                instances = []

                for doc in documents:
                    # Converte todos os valores do MongoDB para Python
                    doc = self.mongo_to_python(doc)

                    # Instancia dinamicamente o dataclass
                    instance = self.dataclass_type(**doc)
                    instances.append(instance)

                # Retorna a primeira instância ou uma lista completa
                return instances[0] if len(instances) == 1 else instances

            def update(self, query: Dict, update_data: Dict) -> Optional[str]:
                """
                Atualiza um documento utilizando $set, ou um pipeline de agregação,
                dependendo do formato de update_data.
                Retorna o id do documento atualizado, ou None se não houver atualização.
                """
                try:
                    # Verifica se update_data tem a estrutura para um pipeline de agregação
                    if isinstance(update_data, list):
                        result = self.collection.update_one(query, update_data)
                    else:
                        result = self.collection.update_one(
                            query, {"$set": update_data}
                        )

                    # Verifica se o documento foi alterado
                    if result.matched_count > 0:
                        updated_doc = self.collection.find_one(query)
                        return str(updated_doc["_id"]) if updated_doc else None

                    return None  # Retorna None caso nenhum documento tenha sido alterado
                except Exception as e:
                    print(f"Error executing update: {e}")
                    return None

            def delete(self, query: Dict) -> int:
                result = self.collection.delete_one(query)
                return result.deleted_count

        return CollectionAccessor(self.db, collection_name, dataclass_type)

    # ---------- Manipulação de Processos ----------
    