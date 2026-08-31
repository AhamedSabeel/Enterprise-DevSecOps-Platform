import os
import time
from datetime import datetime, timezone

import redis
from celery import Celery
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import Counter, Histogram, make_asgi_app
from pydantic import BaseModel
from sqlalchemy import Column, DateTime, Integer, String, create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://enterprise_user:enterprise_password@postgres:5432/enterprise_db"
)

REDIS_URL = os.getenv(
    "REDIS_URL",
    "redis://redis:6379/0"
)


class Base(DeclarativeBase):
    pass


class TaskRecord(Base):
    __tablename__ = "task_records"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    status = Column(String(50), nullable=False, default="pending")
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

Base.metadata.create_all(bind=engine)


redis_client = redis.Redis.from_url(
    REDIS_URL,
    decode_responses=True
)


celery_app = Celery(
    "enterprise_backend",
    broker=REDIS_URL,
    backend=REDIS_URL
)


app = FastAPI(
    title="Enterprise DevSecOps Platform API",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:8080",
        "http://127.0.0.1:8080",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total number of HTTP requests"
)

REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency"
)


class TaskRequest(BaseModel):
    name: str


@app.get("/")
def root():
    return {
        "message": "Enterprise DevSecOps Platform Backend",
        "status": "running"
    }




@app.get("/health")
def health_check():
    database_status = "healthy"
    redis_status = "healthy"

    try:
        with engine.connect() as connection:
            connection.exec_driver_sql("SELECT 1")
    except Exception:  # noqa: BLE001
        database_status = "unhealthy"

    try:
        redis_client.ping()
    except Exception:  # noqa: BLE001
        redis_status = "unhealthy"

    overall_status = (
        "healthy"
        if database_status == "healthy"
        and redis_status == "healthy"
        else "unhealthy"
    )

    return {
        "status": overall_status,
        "service": "backend-api",
        "database": database_status,
        "redis": redis_status,
    }




@app.post("/api/tasks")
def create_task(task: TaskRequest):
    REQUEST_COUNT.inc()

    db = SessionLocal()

    try:
        task_record = TaskRecord(
            name=task.name,
            status="queued"
        )

        db.add(task_record)
        db.commit()
        db.refresh(task_record)

        celery_task = celery_app.send_task(
            "celery_app.process_background_task",
            args=[task.name]
        )

        redis_client.setex(
            f"task:{task_record.id}",
            3600,
            "queued"
        )

        return {
            "id": task_record.id,
            "name": task_record.name,
            "status": task_record.status,
            "celery_task_id": celery_task.id
        }

    finally:
        db.close()


@app.get("/api/tasks")
def list_tasks():
    REQUEST_COUNT.inc()

    db = SessionLocal()

    try:
        tasks = db.query(TaskRecord).all()

        return [
            {
                "id": task.id,
                "name": task.name,
                "status": task.status,
                "created_at": task.created_at
            }
            for task in tasks
        ]

    finally:
        db.close()


@app.get("/api/cache/{key}")
def get_cache(key: str):
    value = redis_client.get(key)

    if value is None:
        raise HTTPException(
            status_code=404,
            detail="Key not found in cache"
        )

    return {
        "key": key,
        "value": value
    }


@app.get("/api/status")
def service_status():
    REQUEST_COUNT.inc()

    start_time = time.time()

    response = {
        "service": "backend-api",
        "status": "operational",
        "timestamp": time.time()
    }

    REQUEST_LATENCY.observe(time.time() - start_time)

    return response


@app.get("/api/simulate-error")
def simulate_error():
    raise HTTPException(
        status_code=500,
        detail="Simulated application error"
    )


metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)
