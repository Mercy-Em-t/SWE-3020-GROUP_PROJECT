from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional

class DepositRequest(BaseModel):
    member_id: int
    amount: float = Field(..., gt=0, description="Deposit amount must be strictly greater than 0")
    phone_number: str = Field(..., pattern=r"^\+?[0-9]{10,15}$")
    payment_channel: Optional[str] = "mpesa"  # "mpesa" or "bank"

class DepositResponse(BaseModel):
    success: bool
    reference_code: str
    amount: float
    new_savings_balance: float
    new_total_shares: float
    timestamp: datetime
    message: str

class SavingsAccountSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    member_id: int
    total_savings: float
    total_shares: float
    borrowing_limit: float
    updated_at: datetime

class LedgerTransactionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    account_id: int
    transaction_type: str
    amount: float
    balance_after: float
    reference_code: str
    description: Optional[str]
    timestamp: datetime
