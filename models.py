from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
from enum import Enum
from datetime import date, datetime

class ClaimStatus(str, Enum):
    DRAFT = "draft"
    PRE_BILL_AUDIT = "pre_bill_audit"
    SUBMITTED = "submitted"
    DENIED = "denied"
    PAID = "paid"
    NEEDS_RESOLUTION = "needs_resolution"

class VulnerabilitySeverity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class Patient(BaseModel):
    id: str
    first_name: str
    last_name: str
    dob: date
    insurance_provider: str
    policy_id: str

class ChargeItem(BaseModel):
    id: str
    cpt_code: str
    description: str
    units: int
    charge_amount: float

class ClaimIngestion(BaseModel):
    hospital_id: str
    hospital_system_claim_id: str
    patient: Patient
    charges: List[ChargeItem]
    admission_date: date
    discharge_date: Optional[date] = None

class VulnerabilityIssue(BaseModel):
    code: str
    description: str
    severity: VulnerabilitySeverity
    recommendation: str

class AuditResponse(BaseModel):
    claim_id: str
    status: str
    vulnerabilities_detected: List[VulnerabilityIssue]
    risk_score: float = Field(..., ge=0, le=100)
    can_submit: bool

class DenialAnalysisRequest(BaseModel):
    claim_id: str
    payer_id: str
    denial_code: str
    remittance_advice: str

class DenialResolutionRecommendation(BaseModel):
    claim_id: str
    recommended_action: str
    success_probability: float
    deployment_automation_status: str = "Awaiting Approval"
    resolution_steps: List[str]
