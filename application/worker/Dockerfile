FROM python:3.12-slim AS builder

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


FROM python:3.12-slim

WORKDIR /app

RUN useradd --create-home appuser

COPY --from=builder /install /usr/local

COPY celery_app.py .

USER appuser

EXPOSE 8002

CMD ["celery", "-A", "celery_app", "worker", "--loglevel=info"]
