FROM python:3.12.1-slim-bookworm

ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH /app/src/bot

RUN apt-get update && apt-get install -y \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY src/ /app/src/

CMD cd /app/src/bot && alembic upgrade head && \
    python -m app