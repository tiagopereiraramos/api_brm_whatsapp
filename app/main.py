from fastapi import FastAPI
from app.api.endpoints.mensagem import router as mensagem_router
from app.api.endpoints.empresa import router as empresa_router

# Cria a aplicação FastAPI
app = FastAPI(
    title="Sistema de Gestão e Envio de Mensagens",
    description="API para envio de mensagens e gestão de empresas utilizando EvolutionService",
    version="1.0.0"
)

# Registra os endpoints de mensagem
app.include_router(mensagem_router, prefix="/api/mensagens",
                   tags=["Mensagens"])

# Registra os endpoints de empresa
app.include_router(empresa_router, prefix="/api/empresas", tags=["Empresas"])

# Endpoint de saúde da aplicação


@app.get("/health", tags=["Health"])
def health_check():
    """
    Endpoint para verificar a saúde da aplicação.
    Retorna status 200 se a aplicação estiver funcionando corretamente.
    """
    return {"status": "ok"}
