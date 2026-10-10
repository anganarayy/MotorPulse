
from datetime import datetime, timezone
from typing import Annotated

from pydantic import BaseModel, Field, ConfigDict


VehicleId = Annotated[
    str,
    Field(min_length=1, max_length=30, pattern=r"^[A-Za-z0-9_-]+$")
]


class TelemetryCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    vehicle_id: VehicleId
    speed_kmh: Annotated[float, Field(ge=0, le=300, allow_inf_nan=False)]
    fuel_level_pct: Annotated[float, Field(ge=0, le=100, allow_inf_nan=False)]
    engine_temp_c: Annotated[float, Field(ge=-50, le=250, allow_inf_nan=False)]


class TelemetryResponse(BaseModel):
    id: int
    vehicle_id: str
    speed_kmh: float
    fuel_level_pct: float
    engine_temp_c: float
    recorded_at: datetime

class TelemetryHistoryResponse(BaseModel):
    vehicle_id: str
    count: int
    readings: list[TelemetryResponse]
