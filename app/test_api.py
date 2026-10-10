
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base
from app.main import app, get_db
from app.main import app


@pytest.fixture
def client():
    test_engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    TestingSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=test_engine,
    )

    Base.metadata.create_all(bind=test_engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=test_engine)
    test_engine.dispose()


def test_health_endpoint(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_create_valid_telemetry(client):
    response = client.post(
        "/telemetry",
        json={
            "vehicle_id": "TEST_VEHICLE",
            "speed_kmh": 60,
            "fuel_level_pct": 70,
            "engine_temp_c": 90,
        },
    )

    assert response.status_code == 201
    assert response.json()["vehicle_id"] == "TEST_VEHICLE"


def test_negative_speed_is_rejected(client):
    response = client.post(
        "/telemetry",
        json={
            "vehicle_id": "TEST_VEHICLE",
            "speed_kmh": -10,
            "fuel_level_pct": 70,
            "engine_temp_c": 90,
        },
    )

    assert response.status_code == 422
