from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.security import (
    get_current_user,
    get_current_admin,
    ensure_self_or_admin,
    is_admin
)
from app.schemas.loan import (
    LoanApplicationRequest,
    LoanEligibilityResponse,
    LoanRepaymentRequest,
    LoanResponse,
    LoanVettingDecision
)
from app.repositories.ledger_repo import LedgerRepository
from app.repositories.loan_repo import LoanRepository
from app.repositories.member_repo import MemberRepository
from app.repositories.audit_repo import AuditRepository
from app.models.entities import Loan, Member, LoanStatus
from app.services.loan_service import LoanCalculationService

router = APIRouter(prefix="/loans", tags=["Credit & Loan Engine"])


def get_loan_calculator() -> LoanCalculationService:
    return LoanCalculationService()


def to_loan_response(loan: Loan) -> LoanResponse:
    """Map a Loan entity to the API read-model, adding borrower name and guarantor count."""
    response = LoanResponse.model_validate(loan)
    response.borrower_name = loan.borrower.full_name if loan.borrower else None
    response.guarantor_count = len(loan.guarantors or [])
    return response


@router.get(
    "/eligibility/{member_id}",
    response_model=LoanEligibilityResponse
)
def check_loan_eligibility(
    member_id: int,
    db: Session = Depends(get_db),
    calculator: LoanCalculationService = Depends(get_loan_calculator),
    current_user: Member = Depends(get_current_user)
):
    ensure_self_or_admin(member_id, current_user)
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
def get_pending_loans(
    db: Session = Depends(get_db),
    _admin: Member = Depends(get_current_admin)
):
    """[Admin] Retrieve all pending loan applications for administrative vetting."""
    return [to_loan_response(loan) for loan in LoanRepository(db).get_pending_loans()]


@router.get("", response_model=List[LoanResponse])
def get_all_loans(
    limit: int = 100,
    db: Session = Depends(get_db),
    _admin: Member = Depends(get_current_admin)
):
    """[Admin] Retrieve all loans (pending, approved, disbursed, closed) for portfolio oversight."""
    return [to_loan_response(loan) for loan in LoanRepository(db).get_all_loans(limit=limit)]


@router.post(
    "/apply",
    response_model=LoanResponse,
    status_code=status.HTTP_201_CREATED
)
def apply_for_loan(
    request: LoanApplicationRequest,
    db: Session = Depends(get_db),
    calculator: LoanCalculationService = Depends(get_loan_calculator),
    current_user: Member = Depends(get_current_user)
):
    ensure_self_or_admin(request.member_id, current_user)

    ledger_repo = LedgerRepository(db)
    loan_repo = LoanRepository(db)
    member_repo = MemberRepository(db)
    audit_repo = AuditRepository(db)

    account = ledger_repo.get_by_member_id(request.member_id)
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Member account not found."
        )

    # 0. Guarantor integrity: must exist, must not be the borrower, no duplicates
    guarantor_ids = [g.guarantor_member_id for g in request.guarantors]
    if request.member_id in guarantor_ids:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You cannot be your own guarantor."
        )
    if len(set(guarantor_ids)) != len(guarantor_ids):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Each guarantor must be a different member."
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

    for gid in guarantor_ids:
        if not member_repo.get_by_id(gid):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Guarantor member {gid} does not exist."
            )

    # 3. Calculate Amortization
    amort = calculator.calculate_amortization(
        principal=request.principal_amount,
        duration_months=request.duration_months
    )

    # Segregation of duties: only an admin/treasurer may auto-approve.
    auto_approve = request.auto_approve and is_admin(current_user)
    initial_status = LoanStatus.APPROVED.value if auto_approve else LoanStatus.PENDING.value
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
        actor_email=current_user.email,
        action="LOAN_SUBMITTED" if initial_status == "PENDING" else "LOAN_APPROVED",
        entity_name="Loan",
        entity_id=created_loan.id,
        delta=(
            f"Principal: KES {created_loan.principal_amount:.2f}, "
            f"Status: {initial_status}"
        )
    )

    db.refresh(created_loan)
    return to_loan_response(created_loan)


@router.post("/{loan_id}/vet", response_model=LoanResponse)
def vet_loan(
    loan_id: int,
    decision: LoanVettingDecision,
    db: Session = Depends(get_db),
    admin: Member = Depends(get_current_admin)
):
    """[Admin] Approve or reject a pending loan application."""
    loan_repo = LoanRepository(db)
    audit_repo = AuditRepository(db)

    loan = loan_repo.get_by_id(loan_id)
    if not loan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Loan with ID {loan_id} not found."
        )
    if loan.status != LoanStatus.PENDING.value:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Loan {loan_id} is already {loan.status}; only PENDING loans can be vetted."
        )
    if loan.member_id == admin.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You cannot vet your own loan application."
        )

    updated_loan = loan_repo.update_loan_status(loan_id, decision.status)
    audit_repo.log_event(
        actor_email=admin.email,
        action=f"LOAN_{decision.status}",
        entity_name="Loan",
        entity_id=loan_id,
        delta=f"Decision: {decision.status}. Notes: {decision.review_notes or 'None'}"
    )
    return to_loan_response(updated_loan)


@router.post("/repay", response_model=LoanResponse)
def repay_loan(
    request: LoanRepaymentRequest,
    db: Session = Depends(get_db),
    current_user: Member = Depends(get_current_user)
):
    loan_repo = LoanRepository(db)
    audit_repo = AuditRepository(db)

    loan = loan_repo.get_by_id(request.loan_id)
    if not loan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Loan with ID {request.loan_id} not found."
        )
    ensure_self_or_admin(loan.member_id, current_user)

    updated_loan = loan_repo.apply_repayment(request.loan_id, request.amount)
    audit_repo.log_event(
        actor_email=current_user.email,
        action="LOAN_REPAYMENT_APPLIED",
        entity_name="Loan",
        entity_id=updated_loan.id,
        delta=(
            f"Paid: KES {request.amount:.2f}, "
            f"Remaining: KES {updated_loan.balance_outstanding:.2f}"
        )
    )
    return to_loan_response(updated_loan)


@router.get("/member/{member_id}", response_model=List[LoanResponse])
def get_member_loans(
    member_id: int,
    db: Session = Depends(get_db),
    current_user: Member = Depends(get_current_user)
):
    ensure_self_or_admin(member_id, current_user)
    return [to_loan_response(loan) for loan in LoanRepository(db).get_member_loans(member_id)]
