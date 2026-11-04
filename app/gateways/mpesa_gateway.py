import uuid
from app.interfaces.payment import IPaymentGateway, PaymentResult

class MpesaDarajaGateway(IPaymentGateway):
    """
    Concrete implementation of IPaymentGateway representing Safaricom Daraja STK Push.
    Open for extension without modifying core ledger services.
    """
    def __init__(self, consumer_key: str = "sandbox_key", consumer_secret: str = "sandbox_secret"):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret

    async def initiate_deposit(self, phone_number: str, amount: float, reference: str) -> PaymentResult:
        # In a real environment, this dispatches an HTTP POST to https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest
        tx_ref = f"DAR_{uuid.uuid4().hex[:10].upper()}"
        return PaymentResult(
            success=True,
            transaction_reference=tx_ref,
            amount=amount,
            message=f"M-Pesa STK Push acknowledged for {phone_number}. Ref: {tx_ref}",
            raw_response={"CheckoutRequestID": f"ws_CO_{uuid.uuid4().hex[:8]}", "ResponseCode": "0"}
        )

    async def disburse_funds(self, phone_number: str, amount: float, reference: str) -> PaymentResult:
        tx_ref = f"B2C_{uuid.uuid4().hex[:10].upper()}"
        return PaymentResult(
            success=True,
            transaction_reference=tx_ref,
            amount=amount,
            message=f"M-Pesa B2C disbursement successful to {phone_number}. Ref: {tx_ref}",
            raw_response={"ConversationID": f"AG_{uuid.uuid4().hex[:8]}", "ResponseCode": "0"}
        )
