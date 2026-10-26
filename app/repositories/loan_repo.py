from typing import Optional, List
from sqlalchemy.orm import Session
from app.repositories.base import BaseRepository
from app.models.entities import Loan, GuarantorCommitment


class LoanRepository(BaseRepository[Loan]):
    def __init__(self, db: Session):
        super().__init__(Loan, db)

    def get_member_loans(self, member_id: int) -> List[Loan]:
        return self.db.query(Loan).filter(Loan.member_id == member_id).all()

    def get_pending_loans(self) -> List[Loan]:
        return self.db.query(Loan).filter(Loan.status == "PENDING").all()

    def add_guarantor(self, loan_id: int, guarantor_id: int, amount: float) -> GuarantorCommitment:
        commitment = GuarantorCommitment(
            loan_id=loan_id,
            guarantor_member_id=guarantor_id,
            amount_guaranteed=amount,
            status="PENDING"
        )
        self.db.add(commitment)
        self.db.commit()
        self.db.refresh(commitment)
        return commitment

    def update_loan_status(self, loan_id: int, status: str) -> Optional[Loan]:
        loan = self.get_by_id(loan_id)
        if loan:
            loan.status = status
            self.db.commit()
            self.db.refresh(loan)
        return loan

    def apply_repayment(self, loan_id: int, amount: float) -> Loan:
        loan = self.get_by_id(loan_id)
        if not loan:
            raise ValueError(f"Loan with ID {loan_id} not found.")

        loan.balance_outstanding = max(0.0, loan.balance_outstanding - amount)
        if loan.balance_outstanding == 0.0:
            loan.status = "CLOSED"
        self.db.commit()
        self.db.refresh(loan)
        return loan
