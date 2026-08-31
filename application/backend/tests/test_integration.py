import os
import time

import requests

BASE_URL = os.getenv(
    "BACKEND_URL",
    "http://localhost:8003"
)


def wait_for_backend(timeout=60):
    start_time = time.time()

    while time.time() - start_time < timeout:
        try:
            response = requests.get(
                f"{BASE_URL}/health",
                timeout=5
            )

            if response.status_code == 200:
                return True

        except requests.RequestException:
            pass

        time.sleep(2)

    return False


def test_backend_health():
    assert wait_for_backend(), "Backend did not become available"

    response = requests.get(
        f"{BASE_URL}/health",
        timeout=10
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "healthy"
    assert data["service"] == "backend-api"
    assert data["database"] == "healthy"
    assert data["redis"] == "healthy"


def test_list_tasks():
    response = requests.get(
        f"{BASE_URL}/api/tasks",
        timeout=10
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)


def test_create_task():
    task_name = "CI Integration Test Task"

    response = requests.post(
        f"{BASE_URL}/api/tasks",
        json={
            "name": task_name
        },
        timeout=10
    )

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == task_name
    assert data["status"] == "queued"
    assert "id" in data
    assert "celery_task_id" in data
