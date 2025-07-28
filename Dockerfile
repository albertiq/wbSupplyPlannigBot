FROM python:3.12.1-slim-bookworm

ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH /app

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY src/ /app/src/
COPY entrypoint.sh /app/

RUN chmod +x /app/entrypoint.sh
ENTRYPOINT ["sh", "/app/entrypoint.sh"]