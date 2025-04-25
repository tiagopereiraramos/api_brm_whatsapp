from motor.motor_asyncio import AsyncIOMotorClient
from app.config.config import getenv
from dataclasses import asdict, is_dataclass
from datetime import datetime
from bson import ObjectId
from typing import Any, Dict, Optional, Type, List
import importlib
import os
import pkgutil


class AsyncDatabase:
    def __init__(self):
        self.uri = getenv("MONGO_URI", "mongodb://localhost:27017")
        self.dbname = getenv("MONGO_DB_NAME", "brm_solutions")
        self.client = AsyncIOMotorClient(self.uri)
        self.db = self.client[self.dbname]
        self.collections = self.load_collections_from_env()

        for name, dataclass_type in self.collections.items():
            setattr(self, name, self._create_collection_accessor(
                name, dataclass_type))

    def load_collections_from_env(self) -> Dict[str, Type]:
        collections_str = getenv("COLLECTIONS", "")
        collections = {}

        if collections_str:
            for item in collections_str.split(","):
                try:
                    collection_name, dataclass_name = item.split(":")
                    dataclass_type = None

                    # Caminho base onde os dataclasses estão organizados
                    base_module_path = "app.models"

                    # Itera sobre os submódulos e arquivos
                    for _, module_name, is_pkg in pkgutil.walk_packages(importlib.import_module(base_module_path).__path__, f"{base_module_path}."):
                        try:
                            # Importa o módulo

                            module = importlib.import_module(module_name)
                            # Verifica se o dataclass está no módulo
                            if hasattr(module, dataclass_name):
                                dataclass_type = getattr(
                                    module, dataclass_name)
                                break
                        except ImportError as e:
                            print(
                                f"Erro ao importar módulo: {module_name}. Detalhes: {e}")

                    if dataclass_type is None:
                        raise ValueError(
                            f"Dataclass {dataclass_name} não encontrado em {base_module_path} ou submódulos.")

                    collections[collection_name] = dataclass_type
                except Exception as e:
                    print(f"Erro ao carregar coleção: {item}. Detalhes: {e}")
        return collections

    def _create_collection_accessor(self, collection_name: str, dataclass_type: Type):
        db = self.db

        class CollectionAccessor:
            def __init__(self):
                self.collection = db[collection_name]
                self.dataclass_type = dataclass_type

            async def create(self, obj: Any) -> str:
                if not is_dataclass(obj):
                    raise TypeError("Esperado dataclass")
                data = asdict(obj)
                if "_id" in data and data["_id"] is None:
                    del data["_id"]
                result = await self.collection.insert_one(data)
                return str(result.inserted_id)

            async def read(self, query: Dict, many: bool = False) -> Any:
                if many:
                    cursor = self.collection.find(query)
                    results = await cursor.to_list(length=100)
                    return [self.dataclass_type(**r) for r in results]
                doc = await self.collection.find_one(query)
                return self.dataclass_type(**doc) if doc else None

            async def update(self, query: Dict, update_data: Dict) -> Optional[str]:
                result = await self.collection.update_one(query, {"$set": update_data})
                if result.matched_count > 0:
                    updated = await self.collection.find_one(query)
                    return str(updated.get("_id")) if updated else None
                return None

            async def delete(self, query: Dict) -> int:
                result = await self.collection.delete_one(query)
                return result.deleted_count

            async def read_all(self, limit: int = 100) -> List[Any]:
                cursor = self.collection.find()
                results = await cursor.to_list(length=limit)
                return [self.dataclass_type(**r) for r in results]

            async def paginate(self, skip: int = 0, limit: int = 20) -> List[Any]:
                cursor = self.collection.find().skip(skip).limit(limit)
                results = await cursor.to_list(length=limit)
                return [self.dataclass_type(**r) for r in results]

            async def exists(self, query: Dict) -> bool:
                count = await self.collection.count_documents(query, limit=1)
                return count > 0

            async def upsert(self, query: Dict, update_data: Dict) -> str:
                result = await self.collection.update_one(query, {"$set": update_data}, upsert=True)
                return str(result.upserted_id or (await self.collection.find_one(query)).get("_id"))

        return CollectionAccessor()


# Exemplo de uso
if __name__ == "__main__":
    from app.models.mensagem.mensagem import Mensagem
    import asyncio

    os.environ["COLLECTIONS"] = "mensagem:Mensagem"

    db = AsyncDatabase()

    async def run():
        dados = await db.mensagem.read_all()
        print(dados)

    asyncio.run(run())
