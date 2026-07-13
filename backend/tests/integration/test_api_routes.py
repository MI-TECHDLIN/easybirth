from __future__ import annotations

from fastapi.testclient import TestClient

from api.main import app


client = TestClient(app)


def test_health_endpoint() -> None:
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_risk_assessment_endpoint() -> None:
    payload = {
        "age_weeks": 28,
        "blood_pressure": 120,
        "heart_rate": 82,
        "weight_kg": 70.5,
        "language": "en",
    }
    response = client.post("/api/v1/risk-assessments", json=payload)
    assert response.status_code == 200
    assert response.json()["risk_level"] == "high"


def test_voice_and_chat_endpoints() -> None:
    voice_response = client.post(
        "/api/v1/voice",
        json={"audio_url": "https://example.com/audio.wav", "language": "en"},
    )
    chat_response = client.post(
        "/api/v1/chat",
        json={"message": "Hello", "language": "en"},
    )

    assert voice_response.status_code == 200
    assert chat_response.status_code == 200
