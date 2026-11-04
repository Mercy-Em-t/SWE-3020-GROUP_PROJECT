from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas.savings import DepositRequest, DepositResponse, SavingsAccountSummary, LedgerTransactionResponse
from app.repositories.ledger_repo import LedgerRepository
from app.repositories.audit_repo import AuditRepository
from app.gateways.mpesa_gateway import MpesaDarajaGateway
from app.gateways.bank_gateway import BankTransferGateway
from app.services.savings_service import SavingsLedgerService
from app.services.loan_service import LoanCalculationService

router = APIRouter(prefix="/savings", tags=["Transactional Core & Ledger"])

def get_savings_service(channel: str = "mpesa", db: Session = Depends(get_db)) -> SavingsLedgerService:
    gateway = BankTransferGateway() if channel.lower() == "bank" else MpesaDarajaGateway()
    return SavingsLedgerService(
        payment_gateway=gateway,
        ledger_repo=LedgerRepository(db),
        audit_repo=AuditRepository(db)
    )

@router.post("/deposit", response_model=DepositResponse)
async def make_deposit(request: DepositRequest, db: Session = Depends(get_db)):
    service = get_savings_service(channel=request.payment_channel or "mpesa", db=db)
    try:
        return await service.process_deposit(request)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/account/{member_id}", response_model=SavingsAccountSummary)
def get_savings_summary(member_id: int, db: Session = Depends(get_db)):
    ledger_repo = LedgerRepository(db)
    account = ledger_repo.get_by_member_id(member_id)
    if not account:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found.")
    
    calculator = LoanCalculationService()
    borrowing_limit = calculator.calculate_borrowing_limit(account.total_shares)

    return SavingsAccountSummary(
        member_id=account.member_id,
        total_savings=account.total_savings,
        total_shares=account.total_shares,
        borrowing_limit=borrowing_limit,
        updated_at=account.updated_at
    )

@router.get("/ledger/{member_id}", response_model=List[LedgerTransactionResponse])
def get_ledger_journal(member_id: int, db: Session = Depends(get_db)):
    ledger_repo = LedgerRepository(db)
    account = ledger_repo.get_by_member_id(member_id)
    if not account:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found.")
    return ledger_repo.get_account_transactions(account.id)
