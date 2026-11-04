import uuid
from app.interfaces.payment import IPaymentGateway, PaymentResult

class BankTransferGateway(IPaymentGateway):
    """
    Alternative IPaymentGateway strategy for Direct Bank Wire/EFT.
    Demonstrates Liskov Substitution Principle (LSP) and Open/Closed Principle (OCP).
    """
    async def initiate_deposit(self, phone_number: str, amount: float, reference: str) -> PaymentResult:
        tx_ref = f"EFT_{uuid.uuid4().hex[:10].upper()}"
        return PaymentResult(
            success=True,
            transaction_reference=tx_ref,
            amount=amount,
            message=f"Direct Bank wire processed. Ref: {tx_ref}",
            raw_response={"BankBatchID": f"BB_{uuid.uuid4().hex[:8]}"}
        )

    async def disburse_funds(self, phone_number: str, amount: float, reference: str) -> PaymentResult:
        tx_ref = f"WIRE_{uuid.uuid4().hex[:10].upper()}"
        return PaymentResult(
            success=True,
            transaction_reference=tx_ref,
            amount=amount,
            message=f"Bank wire disbursement processed. Ref: {tx_ref}",
            raw_response={"WireRef": tx_ref}
        )
