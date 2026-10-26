from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional, List

class GuarantorCommitmentInput(BaseModel):
    guarantor_member_id: int
    amount_guaranteed: float = Field(..., gt=0)

class LoanApplicationRequest(BaseModel):
    member_id: int
    principal_amount: float = Field(..., gt=0)
    duration_months: int = Field(..., ge=1, le=36)
    guarantors: List[GuarantorCommitmentInput] = []

class LoanEligibilityResponse(BaseModel):
    member_id: int
    total_shares: float
    max_borrowing_limit: float
    is_eligible: bool
    rejection_reason: Optional[str] = None

class LoanRepaymentRequest(BaseModel):
    loan_id: int
    amount: float = Field(..., gt=0)
    payment_reference: str

class LoanResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    member_id: int
    principal_amount: float
    interest_rate: float
    duration_months: int
    total_repayable: float
    balance_outstanding: float
    penalty_accumulated: float
    status: str
    created_at: datetime
    due_date: datetime
