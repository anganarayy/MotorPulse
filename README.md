# MotorPulse — Privacy-First Vehicle Telemetry API

MotorPulse is a Python backend project that collects vehicle telemetry, stores readings in SQLite, and generates rule-based alerts for unusual speed and engine temperature values.

## Features

- **Telemetry ingestion:** Accepts vehicle readings through a REST API.
- **Data validation:** Validates vehicle IDs, speed, fuel level, and engine temperature.
- **Vehicle history:** Retrieves recent telemetry readings for a vehicle.
- **Rule-based alerts:** Flags readings that exceed configurable demonstration thresholds.
- **Database persistence:** Uses SQLite and SQLAlchemy.
- **Automated testing:** Uses pytest and FastAPI TestClient to test alert logic and API behavior.
- **Privacy-conscious design:** Uses vehicle identifiers rather than driver names or personal location histories.

## Tech Stack

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- pytest

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Checks service health |
| POST | `/telemetry` | Creates a telemetry reading |
| GET | `/vehicles/{vehicle_id}/telemetry` | Retrieves vehicle history |
| GET | `/alerts` | Retrieves generated alerts, optionally filtered by vehicle |

Interactive API documentation is available at `/docs` when the application is running.

## Run Locally

1. Clone the repository:

   ```bash
   git clone https://github.com/anganarayy/MotorPulse.git
   cd MotorPulse
   ```

2. Create and activate a virtual environment on Windows:

   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   python -m pip install fastapi "uvicorn[standard]" sqlalchemy pytest httpx
   ```

4. Start the API:

   ```bash
   python -m uvicorn app.main:app --reload
   ```

5. Open `http://127.0.0.1:8000/docs`.

## Run Tests

From the project root:

```bash
python -m pytest -v
```

## Alert Thresholds

The current demonstration rules flag speeds above 100 km/h and engine temperatures above 110°C. These values are illustrative and are not manufacturer-specific safety limits.

## Limitations and Future Improvements

- Add integration tests for database persistence and alert retrieval.
- Improve test database isolation and dependency management.
- Add structured logging and consistent error handling.
- Add configurable thresholds and stronger API documentation.
- Add CI using GitHub Actions.

## Disclaimer

MotorPulse is an educational backend project using demonstration thresholds and test data. Its alerts are not a substitute for manufacturer guidance or a vehicle safety system.