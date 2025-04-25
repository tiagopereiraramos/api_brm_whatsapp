# Exemplo de uso
from datetime import datetime
from core.mongo import AsyncDatabase
from models.mensagem.mensagem import Mensagem
from models.empresa.empresa import Empresa, StatusEmpresa
if __name__ == "__main__":

    import asyncio

    db = AsyncDatabase()

    async def run():
        empresa_exemplo = Empresa()
        empresa_exemplo._id = "1234567890abcdef"
        empresa_exemplo.nome = "Empresa Exemplo LTDA"
        empresa_exemplo.status = StatusEmpresa.ATIVA.value
        empresa_exemplo.hash_autenticacao = "abc123def456"
        empresa_exemplo.valor_mensalidade = 500.00
        empresa_exemplo.data_inicio_contrato = datetime(2025, 1, 1)
        empresa_exemplo.data_fim_contrato = datetime(2026, 1, 1)
        empresa_exemplo.ciclo_pagamento = "mensal"
        empresa_exemplo.observacoes = "Cliente em dia com pagamentos"

        empresa = await db.empresa.create(empresa_exemplo)
        print(empresa)

    asyncio.run(run())
