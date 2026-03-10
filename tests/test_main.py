from fastapi.testclient import TestClient
from main import app
import pytest

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["platform_name"] == "AIOrc"

def test_ingest_claim():
    payload = {
        "hospital_id": "HOSP-001",
        "hospital_system_claim_id": "CLM-123",
        "patient": {
            "id": "PAT-001",
            "first_name": "John",
            "last_name": "Doe",
            "dob": "1990-01-01",
            "insurance_provider": "HealthCare Inc",
            "policy_id": "POL-123"
        },
        "charges": [
            {
                "id": "CHG-001",
                "cpt_code": "99213",
                "description": "Office Visit",
                "units": 1,
                "charge_amount": 100.0
            }
        ],
        "admission_date": "2024-03-01"
    }
    response = client.post("/api/v1/claims/ingest", json=payload)
    assert response.status_code == 202
    assert "ingestion_id" in response.json()

def test_pre_audit_failure():
    # Sending a claim with missing discharge date (triggers vulnerability in service logic)
    payload = {
        "hospital_id": "HOSP-001",
        "hospital_system_claim_id": "CLM-456",
        "patient": {
            "id": "PAT-002",
            "first_name": "Jane",
            "last_name": "Doe",
            "dob": "1985-05-05",
            "insurance_provider": "Aetna",
            "policy_id": "POL-456"
        },
        "charges": [
            {
                "id": "CHG-002",
                "cpt_code": "99214",
                "description": "Office Visit",
                "units": 1,
                "charge_amount": 150.0
            }
        ],
        "admission_date": "2024-03-05"
    }
    response = client.post("/api/v1/claims/pre-audit", json=payload)
    assert response.status_code == 200
    result = response.json()
    assert result["can_submit"] is False
    assert len(result["vulnerabilities_detected"]) > 0

def test_revenue_optimization():
    payload = {
        "facility_id": "FAC-001",
        "start_date": "2024-01-01",
        "end_date": "2024-03-01"
    }
    response = client.post("/api/v1/revenue/optimize", json=payload)
    assert response.status_code == 200
    result = response.json()
    assert result["total_potential_gain"] > 0
    assert len(result["strategies"]) == 3
