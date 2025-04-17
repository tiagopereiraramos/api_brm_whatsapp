from fastapi import FastAPI
from app.api.endpoints import empresa, cobrancas, whatsapp, templates

app = FastAPI(title="API de Cobranças com RabbitMQ")

app.include_router(empresa.router, prefix="/empresas", tags=["Empresas"])
app.include_router(cobrancas.router, prefix="/mensagens", tags=["Mensagens"])
app.include_router(whatsapp.router, prefix="/whatsapp", tags=["WhatsApp"])
