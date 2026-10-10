
from app.models import Telemetry

# Demonstration thresholds only.
OVERSPEED_THRESHOLD_KMH = 100
HIGH_ENGINE_TEMP_C = 110


def evaluate_telemetry(reading: Telemetry) -> list[dict]:
    alerts = []

    if reading.speed_kmh > OVERSPEED_THRESHOLD_KMH:
        alerts.append({
            "type": "OVERSPEED",
            "severity": "warning",
            "message": (
                f"Reported speed is {reading.speed_kmh} km/h, "
                f"above the configured threshold of "
                f"{OVERSPEED_THRESHOLD_KMH} km/h."
            ),
            "recommended_action": (
                "Verify the reading and assess it against "
                "the applicable road speed limit."
            ),
        })

    if reading.engine_temp_c > HIGH_ENGINE_TEMP_C:
        alerts.append({
            "type": "HIGH_ENGINE_TEMPERATURE",
            "severity": "critical",
            "message": (
                f"Reported engine temperature is "
                f"{reading.engine_temp_c}°C, above the "
                f"configured threshold of {HIGH_ENGINE_TEMP_C}°C."
            ),
            "recommended_action": (
                "Verify the sensor reading and follow the "
                "manufacturer's guidance."
            ),
        })

    return alerts
