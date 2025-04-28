# Etapa base com Python 3.13 em imagem leve
FROM python:3.11-slim-bullseye AS base

# Instala dependências do sistema necessárias para build de pacotes Python
RUN apt-get update && apt-get install -y \
    curl gcc libpq-dev build-essential \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Instala o uv-pip (gerenciador de dependências moderno)
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# Adiciona o diretório do uv ao PATH
ENV PATH="/root/.local/bin:${PATH}"

# Define o diretório de trabalho no container
WORKDIR /app

# Copia todos os arquivos do projeto para o container
COPY . .

# Garante que o uv está instalado no ambiente e restaura as dependências
RUN pip install --no-cache-dir uv && uv venv && .venv/bin/uv pip install -r requirements.txt || true && uv pip install .

# Define variáveis de ambiente (substitua por variáveis no docker-compose.yml para produção)
ENV CELERY_BROKER_URL=redis://redis:6379 \
    CELERY_RESULT_BACKEND=redis://redis:6379 \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Expõe a porta da aplicação
EXPOSE 8000

# Comando padrão: inicia worker, flower e uvicorn
CMD ["sh", "-c", "\
    .venv/bin/celery -A app.celery_worker.celery_app worker --loglevel=info & \
    .venv/bin/celery -A app.tasks flower --port=5555 & \
    .venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000"]
