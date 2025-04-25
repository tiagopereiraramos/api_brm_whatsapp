from celery import Celery
from app.config.config import getenv

CELERY_BROKER_URL = getenv(
    "CELERY_BROKER_URL", "server.brmsolutions.com.br:6379")
CELERY_RESULT_BACKEND = getenv("CELERY_RESULT_BACKEND", "rpc://")

celery_app = Celery(
    "app",
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND,
    include=["app.tasks.enviar_mensagem_task"]
)


# Fila padrão
celery_app.conf.task_default_queue = "mensagens"
