
from contextlib import asynccontextmanager
from datetime import datetime, timezone

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy.orm import Session

from app import models
from app.alerts import evaluate_telemetry
from app.database import Base, SessionLocal, engine
from app.schemas import (
    TelemetryCreate,
    TelemetryHistoryResponse,
    TelemetryResponse,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="MotorPulse",
    description="Privacy-first connected vehicle monitoring API",
    version="1.0.0",
    lifespan=lifespan,
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "MotorPulse",
    }


@app.post(
    "/telemetry",
    response_model=TelemetryResponse,
    status_code=201,
)
def create_telemetry(
    payload: TelemetryCreate,
    db: Session = Depends(get_db),
):
    reading = models.Telemetry(
        vehicle_id=payload.vehicle_id,
        speed_kmh=payload.speed_kmh,
        fuel_level_pct=payload.fuel_level_pct,
        engine_temp_c=payload.engine_temp_c,
        recorded_at=datetime.now(timezone.utc),
    )

    try:
        db.add(reading)
        db.commit()
        db.refresh(reading)
        return reading
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Unable to store telemetry",
        )


@app.get(
    "/vehicles/{vehicle_id}/telemetry",
    response_model=TelemetryHistoryResponse,
)
def get_vehicle_telemetry(
    vehicle_id: str,
    limit: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    readings = (
        db.query(models.Telemetry)
        .filter(models.Telemetry.vehicle_id == vehicle_id)
        .order_by(
            models.Telemetry.recorded_at.desc(),
            models.Telemetry.id.desc(),
        )
        .limit(limit)
        .all()
    )

    return {
        "vehicle_id": vehicle_id,
        "count": len(readings),
        "readings": readings,
    }


@app.get("/alerts")
def get_alerts(
    vehicle_id: str | None = None,
    db: Session = Depends(get_db),
):
    query = db.query(models.Telemetry)

    if vehicle_id:
        query = query.filter(
            models.Telemetry.vehicle_id == vehicle_id
        )

    readings = (
        query.order_by(
            models.Telemetry.recorded_at.desc(),
            models.Telemetry.id.desc(),
        )
        .limit(100)
        .all()
    )

    results = []

    for reading in readings:
        for alert in evaluate_telemetry(reading):
            results.append({
                "telemetry_id": reading.id,
                "vehicle_id": reading.vehicle_id,
                "recorded_at": reading.recorded_at,
                **alert,
            })

    return {
        "count": len(results),
        "alerts": results,
    }
