from datetime import datetime, timezone
from app.interfaces.payment import IPaymentGateway
from app.repositories.ledger_repo import LedgerRepository
from app.repositories.audit_repo import AuditRepository
from app.schemas.savings import DepositRequest, DepositResponse

class SavingsLedgerService:
    """
    Dependency Inversion Principle (DIP):
    Depends upon IPaymentGateway and repository interfaces rather than concrete implementations.
    """
    def __init__(
        self,
        payment_gateway: IPaymentGateway,
        ledger_repo: LedgerRepository,
        audit_repo: AuditRepository
    ):
        self.gateway = payment_gateway
        self.ledger_repo = ledger_repo
        self.audit_repo = audit_repo

    async def process_deposit(self, request: DepositRequest, actor_email: str = "system") -> DepositResponse:
        account = self.ledger_repo.get_by_member_id(request.member_id)
        if not account:
            raise ValueError(f"Savings account for member ID {request.member_id} does not exist.")

        # 1. Dispatch through pluggable payment gateway strategy (M-Pesa / Bank)
        payment_res = await self.gateway.initiate_deposit(
            phone_number=request.phone_number,
            amount=request.amount,
            reference=f"DEP-{account.id}-{int(datetime.now(timezone.utc).timestamp())}"
        )

        if not payment_res.success:
            raise RuntimeError(f"Payment gateway failed: {payment_res.message}")

        # 2. Enforce ACID double-entry balance update & ledger record
        tx = self.ledger_repo.record_deposit(
            account_id=account.id,
            amount=request.amount,
            reference_code=payment_res.transaction_reference,
            description=f"Savings deposit via {request.payment_channel.upper()}"
        )

        # 3. Append forensic audit log
        self.audit_repo.log_event(
            actor_email=actor_email,
            action="DEPOSIT_COMPLETED",
            entity_name="LedgerTransaction",
            entity_id=tx.id,
            delta=f"+KES {request.amount:.2f} (New Balance: KES {tx.balance_after:.2f})"
        )

        return DepositResponse(
            success=True,
            reference_code=tx.reference_code,
            amount=tx.amount,
            new_savings_balance=account.total_savings,
            new_total_shares=account.total_shares,
            timestamp=tx.timestamp,
            message="Savings deposit processed and verified successfully."
        )
