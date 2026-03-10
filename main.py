from fastapi import FastAPI, HTTPException, Depends
from models import ClaimIngestion, AuditResponse, DenialAnalysisRequest, DenialResolutionRecommendation
from services import AIOrchestrationService
from typing import Dict, Any

app = FastAPI(
    title="AIOrc Backend - Revenue Cycle Management API",
    description="Sample AI Orchestration platform for healthcare payments and hospital system integration.",
    version="1.0.0"
)

# -----------------
# Root Endpoint
# -----------------
@app.get("/")
async def root():
    return {
        "platform_name": "AIOrc",
        "mission": "Maximize revenue outcomes for healthcare providers with AI Orchestration.",
        "api_status": "Healthy",
        "features": [
            "Real-time Pre-bill Audit",
            "Automated Denial Resolution",
            "EHR Integration Data Ingestion"
        ]
    }

# -----------------
# API 1: Data Ingestion (Hospital to Adonis)
# -----------------
@app.post("/api/v1/claims/ingest", status_code=202)
async def ingest_claim(claim: ClaimIngestion) -> Dict[str, Any]:
    """
    Exposes an endpoint for a hospital's EHR system to ingest claim and patient data. 
    Following the Medallion architecture, this stages data in the Bronze layer.
    """
    try:
        result = await AIOrchestrationService.ingest_hospital_data(claim)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# -----------------
# API 2: Pre-bill Audit (Vulnerability Detection)
# -----------------
@app.post("/api/v1/claims/pre-audit", response_model=AuditResponse)
async def pre_bill_audit(claim: ClaimIngestion) -> AuditResponse:
    """
    Detect vulnerabilities and billing errors before submitting a claim to a payer.
    Uses AI to recommend tailoring resolutions to maximize revenue outcomes.
    """
    try:
        audit_result = await AIOrchestrationService.pre_bill_audit(claim)
        return audit_result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Audit process failed: {str(e)}")

# -----------------
# API 3: Denial Resolution Analysis
# -----------------
@app.post("/api/v1/denials/analyze", response_model=DenialResolutionRecommendation)
async def analyze_denial(request: DenialAnalysisRequest) -> DenialResolutionRecommendation:
    """
    Analyzes a payer-denied claim to provide recommended steps for resolution.
    Initiates Temporal workflows for automated resolution deployment.
    """
    try:
        recommendation = await AIOrchestrationService.analyze_denial_for_resolution(request)
        return recommendation
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Denial analysis failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
