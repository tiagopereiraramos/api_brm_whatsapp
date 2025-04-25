from app.celery_worker import celery_app


@celery_app.task(name="enviar_mensagem_task", queue="mensagens")
def enviar_mensagem_task(numero: str, texto: str) -> dict:
    from app.services.evolution_service import EvolutionService
    from app.config.config import getenv

    service = EvolutionService(
        base_url=getenv("EVOLUTION_BASE_URL"),
        apikey=getenv("EVOLUTION_API_KEY"),
        instance=getenv("EVOLUTION_API_INSTANCE")
    )

    return service.send_text_message(number=numero, text=texto)
