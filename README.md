# AIOrc Backend - Revenue Cycle Management (RCM) API

This is a sample Python backend for **AIOrc**, an AI Orchestration platform for healthcare payments. The API is designed for integration with hospital systems (EHRs) to optimize the revenue cycle by detecting billing vulnerabilities and automating denial resolutions.

## Features
- **Data Ingestion**: Staging hospital and patient data into the Medallion architecture (Bronze layer).
- **Pre-bill Audit**: Real-time AI vulnerability detection before claim submission to payers.
- **Denial Resolution**: AI-driven analysis of denied claims with automated resolution workflows (Temporal-ready).
- **Revenue Optimization**: Identify revenue leaks and actionable strategies to maximize outcomes.

## Tech Stack
- **FastAPI**: Modern, high-performance web framework.
- **Pydantic**: Robust data validation and settings management.
- **Uvicorn**: Lightning-fast ASGI server.

## Getting Started

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Server
```bash
python main.py
```
The API will be available at `http://127.0.0.1:8000`.

### 3. API Documentation
Once the server is running, you can explore the interactive API docs:
- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## Example API Integrations

### 1. Ingest Hospital Claim (POST `/api/v1/claims/ingest`)
```json
{
  "hospital_id": "HOSP-001",
  "hospital_system_claim_id": "CLM-99234",
  "patient": {
    "id": "PAT-112",
    "first_name": "John",
    "last_name": "Smith",
    "dob": "1985-05-15",
    "insurance_provider": "Blue Cross Blue Shield",
    "policy_id": "POL-8822"
  },
  "charges": [
    {
      "id": "CHG-001",
      "cpt_code": "99213",
      "description": "Office Visit - Level 3",
      "units": 1,
      "charge_amount": 150.00
    }
  ],
  "admission_date": "2024-03-20"
}
```

### 2. Run Pre-bill Audit (POST `/api/v1/claims/pre-audit`)
Use the same JSON payload as the ingestion endpoint to detect vulnerabilities. The AI will return a risk score and submission recommendations.

### 3. Analyze Denial Resolution (POST `/api/v1/denials/analyze`)
```json
{
  "claim_id": "CLM-99234",
  "payer_id": "PAYER-01",
  "denial_code": "CO-16",
  "remittance_advice": "Claim lacks information or has a submission/billing error which is needed for adjudication."
}
```
