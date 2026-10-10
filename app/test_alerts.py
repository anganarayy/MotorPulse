
from types import SimpleNamespace

from app.alerts import evaluate_telemetry


def make_reading(speed_kmh=60, engine_temp_c=90):
    return SimpleNamespace(
        speed_kmh=speed_kmh,
        engine_temp_c=engine_temp_c,
    )


def test_normal_reading_has_no_alerts():
    reading = make_reading(60, 90)

    assert evaluate_telemetry(reading) == []


def test_overspeed_alert():
    reading = make_reading(120, 90)

    alerts = evaluate_telemetry(reading)

    assert len(alerts) == 1
    assert alerts[0]["type"] == "OVERSPEED"


def test_high_temperature_alert():
    reading = make_reading(60, 115)

    alerts = evaluate_telemetry(reading)

    assert len(alerts) == 1
    assert alerts[0]["type"] == "HIGH_ENGINE_TEMPERATURE"


def test_both_alerts():
    reading = make_reading(120, 115)

    alerts = evaluate_telemetry(reading)

    assert len(alerts) == 2
