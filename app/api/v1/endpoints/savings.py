from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.security import get_current_user, get_current_admin, ensure_self_or_admin
from app.models.entities import Member
from app.schemas.savings import (
    DepositRequest,
    DepositResponse,
    SavingsAccountSummary,
    LedgerTransactionResponse,
    GroupFinancialSummary
)
from app.repositories.ledger_repo import LedgerRepository
from app.repositories.audit_repo import AuditRepository
from app.repositories.loan_repo import LoanRepository
from app.repositories.member_repo import MemberRepository
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
async def make_deposit(
    request: DepositRequest,
    db: Session = Depends(get_db),
    current_user: Member = Depends(get_current_user)
):
    ensure_self_or_admin(request.member_id, current_user)
    service = get_savings_service(channel=request.payment_channel or "mpesa", db=db)
    try:
        return await service.process_deposit(request, actor_email=current_user.email)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/account/{member_id}", response_model=SavingsAccountSummary)
def get_savings_summary(
    member_id: int,
    db: Session = Depends(get_db),
    current_user: Member = Depends(get_current_user)
):
    ensure_self_or_admin(member_id, current_user)
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
def get_ledger_journal(
    member_id: int,
    db: Session = Depends(get_db),
    current_user: Member = Depends(get_current_user)
):
    ensure_self_or_admin(member_id, current_user)
    ledger_repo = LedgerRepository(db)
    account = ledger_repo.get_by_member_id(member_id)
    if not account:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found.")
    
    txs = ledger_repo.get_account_transactions(account.id)
    responses = []
    for tx in txs:
        resp = LedgerTransactionResponse.model_validate(tx)
        resp.member_name = account.member.full_name if account.member else None
        responses.append(resp)
    return responses


@router.get("/transactions", response_model=List[LedgerTransactionResponse])
def get_all_group_transactions(
    limit: int = 100,
    db: Session = Depends(get_db),
    _admin: Member = Depends(get_current_admin)
):
    """[Admin] Retrieve all group deposits and transactions for reconciliation."""
    ledger_repo = LedgerRepository(db)
    txs = ledger_repo.get_all_transactions(limit=limit)
    responses = []
    for tx in txs:
        resp = LedgerTransactionResponse.model_validate(tx)
        resp.member_name = tx.account.member.full_name if tx.account and tx.account.member else "Unknown"
        responses.append(resp)
    return responses


@router.get("/summary", response_model=GroupFinancialSummary)
def get_group_summary(
    db: Session = Depends(get_db),
    _admin: Member = Depends(get_current_admin)
):
    """[Admin] Retrieve top-level aggregates for the Admin Dashboard."""
    ledger_repo = LedgerRepository(db)
    loan_repo = LoanRepository(db)
    member_repo = MemberRepository(db)

    accounts = ledger_repo.list_all(limit=1000)
    total_savings = sum(a.total_savings for a in accounts)
    pending_loans = len(loan_repo.get_pending_loans())
    members = member_repo.list_all(limit=1000)
    all_txs = ledger_repo.get_all_transactions(limit=100)

    return GroupFinancialSummary(
        total_group_savings=total_savings,
        pending_loan_approvals=pending_loans,
        total_members=len(members),
        recent_transactions_count=len(all_txs)
    )
