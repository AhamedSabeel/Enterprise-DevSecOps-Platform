import os
import sys
from pathlib import Path
from unittest.mock import MagicMock

# Add backend directory to Python path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# Use SQLite for testing instead of PostgreSQL
os.environ["DATABASE_URL"] = "sqlite:///./test.db"

from fastapi.testclient import TestClient

import main

client = TestClient(main.app)


def test_root():
    response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "Enterprise DevSecOps Platform Backend"
    assert data["status"] == "running"


def test_service_status():
    response = client.get("/api/status")

    assert response.status_code == 200

    data = response.json()

    assert data["service"] == "backend-api"
    assert data["status"] == "operational"
    assert "timestamp" in data


def test_simulate_error():
    response = client.get("/api/simulate-error")

    assert response.status_code == 500

    data = response.json()

    assert data["detail"] == "Simulated application error"


def test_cache_not_found(monkeypatch):
    mock_redis = MagicMock()
    mock_redis.get.return_value = None

    monkeypatch.setattr(main, "redis_client", mock_redis)

    response = client.get("/api/cache/test-key")

    assert response.status_code == 404

    data = response.json()

    assert data["detail"] == "Key not found in cache"
