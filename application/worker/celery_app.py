from celery import Celery
from prometheus_client import Counter, start_http_server
import time
import os


REDIS_URL = os.getenv(
    "REDIS_URL",
    "redis://redis:6379/0"
)

celery_app = Celery(
    "enterprise_worker",
    broker=REDIS_URL,
    backend=REDIS_URL
)


TASK_COUNTER = Counter(
    "background_tasks_total",
    "Total number of background tasks processed"
)


@celery_app.task
def process_background_task(task_name):
    TASK_COUNTER.inc()

    print(f"Processing background task: {task_name}")

    time.sleep(2)

    return {
        "task": task_name,
        "status": "completed"
    }


if __name__ == "__main__":
    start_http_server(8002)

    celery_app.worker_main([
        "worker",
        "--loglevel=info"
    ])
