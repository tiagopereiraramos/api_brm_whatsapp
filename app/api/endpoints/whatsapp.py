from fastapi import APIRouter

router = APIRouter()

@router.post("/configuracao")
async def configurar_whatsapp(config: dict):
    return {"message": "Configuração do WhatsApp salva com sucesso", "data": config}

@router.get("/configuracao")
async def obter_configuracao_whatsapp():
    return {"message": "Configuração do WhatsApp obtida com sucesso"}