from abc import ABC, abstractmethod
from pydantic import BaseModel
from typing import Optional

class PaymentResult(BaseModel):
    success: bool
    transaction_reference: str
    amount: float
    message: str
    raw_response: Optional[dict] = None

class IPaymentGateway(ABC):
    """
    Open/Closed Principle (OCP) & Interface Segregation (ISP):
    Pluggable payment provider contract.
    """
    @abstractmethod
    async def initiate_deposit(self, phone_number: str, amount: float, reference: str) -> PaymentResult:
        """Trigger an inbound contribution/deposit via STK push or bank wire."""
        pass

    @abstractmethod
    async def disburse_funds(self, phone_number: str, amount: float, reference: str) -> PaymentResult:
        """Trigger an outbound B2C loan disbursement."""
        pass
