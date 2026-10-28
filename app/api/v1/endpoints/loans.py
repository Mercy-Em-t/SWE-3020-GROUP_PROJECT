from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas.loan import (
    LoanApplicationRequest,
    LoanEligibilityResponse,
    LoanRepaymentRequest,
    LoanResponse,
    LoanVettingDecision
)
from app.repositories.ledger_repo import LedgerRepository
from app.repositories.loan_repo import LoanRepository
from app.repositories.audit_repo import AuditRepository
from app.models.entities import Loan
from app.services.loan_service import LoanCalculationService

router = APIRouter(prefix="/loans", tags=["Credit & Loan Engine"])


def get_loan_calculator() -> LoanCalculationService:
    return LoanCalculationService()


@router.get(
    "/eligibility/{member_id}",
    response_model=LoanEligibilityResponse
)
def check_loan_eligibility(
    member_id: int,
    db: Session = Depends(get_db),
    calculator: LoanCalculationService = Depends(get_loan_calculator)
):
    account = LedgerRepository(db).get_by_member_id(member_id)
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Member account not found."
        )

    max_limit = calculator.calculate_borrowing_limit(account.total_shares)
    is_eligible = max_limit > 0

    return LoanEligibilityResponse(
        member_id=member_id,
        total_shares=account.total_shares,
        max_borrowing_limit=max_limit,
        is_eligible=is_eligible,
        rejection_reason=None if is_eligible else "Insufficient shares."
    )


@router.get("/pending", response_model=List[LoanResponse])
def get_pending_loans(db: Session = Depends(get_db)):
    """Retrieve all pending loan applications for administrative vetting."""
    return LoanRepository(db).get_pending_loans()


@router.post(
    "/apply",
    response_model=LoanResponse,
    status_code=status.HTTP_201_CREATED
)
def apply_for_loan(
    request: LoanApplicationRequest,
    db: Session = Depends(get_db),
    calculator: LoanCalculationService = Depends(get_loan_calculator)
):
    ledger_repo = LedgerRepository(db)
    loan_repo = LoanRepository(db)
    audit_repo = AuditRepository(db)

    account = ledger_repo.get_by_member_id(request.member_id)
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Member account not found."
        )

    # 1. Enforce Borrowing Threshold (3x Shares)
    max_limit = calculator.calculate_borrowing_limit(account.total_shares)
    if request.principal_amount > max_limit:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                f"Requested principal KES {request.principal_amount:.2f} "
                f"exceeds allowable limit of KES {max_limit:.2f}"
            )
        )

    # 2. Enforce Guarantor Sufficiency
    guarantors_data = [
        {"amount": g.amount_guaranteed} for g in request.guarantors
    ]
    if not calculator.validate_guarantor_coverage(
        request.principal_amount,
        account.total_shares,
        guarantors_data
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsecured loan portion exceeds committed guarantor coverage."
        )

    # 3. Calculate Amortization
    amort = calculator.calculate_amortization(
        principal=request.principal_amount,
        duration_months=request.duration_months
    )

    initial_status = "APPROVED" if request.auto_approve else "PENDING"
    due = datetime.now(timezone.utc) + timedelta(
        days=30 * request.duration_months
    )

    loan = Loan(
        member_id=request.member_id,
        principal_amount=request.principal_amount,
        interest_rate=amort["annual_interest_rate"],
        duration_months=request.duration_months,
        total_repayable=amort["total_repayable"],
        balance_outstanding=amort["total_repayable"],
        status=initial_status,
        due_date=due
    )
    created_loan = loan_repo.create(loan)

    # Attach guarantors
    for g in request.guarantors:
        loan_repo.add_guarantor(
            created_loan.id,
            g.guarantor_member_id,
            g.amount_guaranteed
        )

    audit_repo.log_event(
        actor_email="system",
        action="LOAN_SUBMITTED" if initial_status == "PENDING" else "LOAN_APPROVED",
        entity_name="Loan",
        entity_id=created_loan.id,
        delta=(
            f"Principal: KES {created_loan.principal_amount:.2f}, "
            f"Status: {initial_status}"
        )
    )

    return created_loan


@router.post("/{loan_id}/vet", response_model=LoanResponse)
def vet_loan(
    loan_id: int,
    decision: LoanVettingDecision,
    db: Session = Depends(get_db)
):
    """Admin endpoint to approve or reject a pending loan application."""
    loan_repo = LoanRepository(db)
    audit_repo = AuditRepository(db)

    loan = loan_repo.get_by_id(loan_id)
    if not loan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Loan with ID {loan_id} not found."
        )

    updated_loan = loan_repo.update_loan_status(loan_id, decision.status)
    audit_repo.log_event(
        actor_email="admin@sacco.test",
        action=f"LOAN_{decision.status}",
        entity_name="Loan",
        entity_id=loan_id,
        delta=f"Decision: {decision.status}. Notes: {decision.review_notes or 'None'}"
    )
    return updated_loan


@router.post("/repay", response_model=LoanResponse)
def repay_loan(
    request: LoanRepaymentRequest,
    db: Session = Depends(get_db)
):
    loan_repo = LoanRepository(db)
    audit_repo = AuditRepository(db)

    try:
        updated_loan = loan_repo.apply_repayment(
            request.loan_id,
            request.amount
        )
        audit_repo.log_event(
            actor_email="system",
            action="LOAN_REPAYMENT_APPLIED",
            entity_name="Loan",
            entity_id=updated_loan.id,
            delta=(
                f"Paid: KES {request.amount:.2f}, "
                f"Remaining: KES {updated_loan.balance_outstanding:.2f}"
            )
        )
        return updated_loan
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.get("/member/{member_id}", response_model=List[LoanResponse])
def get_member_loans(member_id: int, db: Session = Depends(get_db)):
    return LoanRepository(db).get_member_loans(member_id)
