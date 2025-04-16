
# 📘 Documentação Técnica — API de Envio de Mensagens via WhatsApp

## 📌 Visão Geral

Este projeto consiste em uma **API em FastAPI** com foco em envio de mensagens via **WhatsApp** para múltiplas empresas (ex: colégios).  
Cada empresa tem uma base lógica separada, com configuração própria, recorrência de pagamento e chave de autenticação.  
Mensagens, configurações e métricas são armazenadas no **MongoDB**. Boletos e arquivos são armazenados no **MinIO**.

---

## 🧱 Arquitetura do Projeto

```text
FastAPI (REST)           <- Interface principal
└── Redis/RabbitMQ       <- Fila de mensagens para envio assíncrono
    └── Worker(s)        <- Consome fila e envia mensagens
        └── WhatsApp API <- Serviço de envio real (oficial ou Evolution)
MongoDB                  <- Armazena dados das empresas, mensagens e métricas
MinIO                    <- Armazena boletos e arquivos
```

---

## 🗃️ Estrutura das Collections (MongoDB)

Cada empresa possui uma instância lógica isolada, representada por sua própria base de dados MongoDB.

### 🔹 Tabela: `empresa`

| Campo             | Tipo     | Descrição |
|------------------|----------|-----------|
| `_id`            | str      | ID Mongo |
| `nome`           | str      | Nome da empresa |
| `status`         | Enum     | `ativo` ou `inativo` |
| `hash_autenticacao` | str  | Chave usada para validar chamadas à API |
| `valor_mensalidade` | float | Valor mensal cobrado |

### 🔹 Tabela: `mensagem`

| Campo           | Tipo     | Descrição |
|----------------|----------|-----------|
| `_id`          | str      | ID Mongo |
| `empresa_id`   | str      | Referência para empresa |
| `numero_destino` | str    | Número do WhatsApp |
| `template`     | str      | Nome do template usado |
| `payload`      | dict     | Dados dinâmicos da mensagem |
| `status_envio` | Enum     | `sucesso`, `erro`, `pendente` |
| `tentativas`   | int      | Número de tentativas de envio |
| `data_envio`   | datetime | Quando foi enviado |

### 🔹 Tabela: `configuracao_whatsapp`

| Campo              | Tipo     | Descrição |
|-------------------|----------|-----------|
| `_id`             | str      | ID Mongo |
| `empresa_id`      | str      | Referência para empresa |
| `tipo`            | Enum     | `oficial` ou `evolution` |
| `token`           | str      | Token de autenticação |
| `remetente_padrao` | str     | Número do remetente |

### 🔹 Tabela: `relatorio_mensal`

| Campo         | Tipo     | Descrição |
|---------------|----------|-----------|
| `_id`        | str      | ID Mongo |
| `empresa_id` | str      | Referência para empresa |
| `mes_ano`    | str      | Ex: `2025-04` |
| `total_enviadas` | int  | Total de mensagens |
| `total_sucesso`  | int  | Mensagens com sucesso |
| `total_erro`     | int  | Mensagens com falha |

---

## 🧾 Dataclasses

```python
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional, Dict

class StatusEmpresa(str, Enum):
    ATIVO = "ativo"
    INATIVO = "inativo"

@dataclass
class Empresa:
    _id: Optional[str]
    nome: str
    status: StatusEmpresa
    hash_autenticacao: str
    valor_mensalidade: float

class StatusEnvio(str, Enum):
    SUCESSO = "sucesso"
    ERRO = "erro"
    PENDENTE = "pendente"

@dataclass
class Mensagem:
    _id: Optional[str]
    empresa_id: str
    numero_destino: str
    template: str
    payload: Dict[str, str]
    status_envio: StatusEnvio
    tentativas: int
    data_envio: Optional[datetime] = None

class TipoWhatsapp(str, Enum):
    OFICIAL = "oficial"
    EVOLUTION = "evolution"

@dataclass
class ConfiguracaoWhatsapp:
    _id: Optional[str]
    empresa_id: str
    tipo: TipoWhatsapp
    token: str
    remetente_padrao: str

@dataclass
class RelatorioMensal:
    _id: Optional[str]
    empresa_id: str
    mes_ano: str
    total_enviadas: int
    total_sucesso: int
    total_erro: int
```

---

## 🛠️ Classe de Acesso ao MongoDB

Você já possui uma poderosa classe `Database` que gera dinamicamente os acessos com base nas dataclasses e nos nomes das coleções.

---

## 🧪 Factory de Coleções com Tipagem

```python
from database import Database
from util.dataclass import Empresa, Mensagem, ConfiguracaoWhatsapp, RelatorioMensal
from typing import Type, Dict

class MongoHandlerFactory:
    _map: Dict[str, Type] = {
        "empresa": Empresa,
        "mensagem": Mensagem,
        "configuracao_whatsapp": ConfiguracaoWhatsapp,
        "relatorio_mensal": RelatorioMensal,
    }

    def __init__(self):
        self.db = Database()

    def get(self, nome: str):
        if nome not in self._map:
            raise ValueError(f"Collection '{nome}' não está registrada.")
        return getattr(self.db, nome)

# Exemplo de uso:
factory = MongoHandlerFactory()
mensagem_handler = factory.get("mensagem")
```

---

## ☁️ MinIO para Armazenamento de Boletos

O MinIO já está configurado no projeto, com service Python pronto para upload e recuperação de boletos, que serão referenciados nas mensagens ou payloads.

---

## ✅ Próximos Passos

- [ ] Criar endpoints REST para receber requisições autenticadas com hash da empresa.
- [ ] Implementar mecanismo de fila com Redis ou RabbitMQ para envio assíncrono.
- [ ] Worker com retries e integração com o serviço WhatsApp.
- [ ] Criação automática dos `relatorio_mensal` por empresa.
- [ ] Dashboard via Metabase com métricas mensais.
