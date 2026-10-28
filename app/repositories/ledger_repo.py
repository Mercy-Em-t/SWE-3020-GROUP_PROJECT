from typing import Optional, List
from sqlalchemy.orm import Session
from app.repositories.base import BaseRepository
from app.models.entities import SavingsAccount, LedgerTransaction

class LedgerRepository(BaseRepository[SavingsAccount]):
    def __init__(self, db: Session):
        super().__init__(SavingsAccount, db)

    def get_by_member_id(self, member_id: int) -> Optional[SavingsAccount]:
        return self.db.query(SavingsAccount).filter(SavingsAccount.member_id == member_id).first()

    def record_deposit(self, account_id: int, amount: float, reference_code: str, description: str) -> LedgerTransaction:
        """
        Enforce ACID Atomicity:
        1. Lock & increment SavingsAccount balance and shares.
        2. Append immutable record to LedgerTransaction table.
        """
        account = self.get_by_id(account_id)
        if not account:
            raise ValueError(f"Account with ID {account_id} not found.")

        account.total_savings += amount
        account.total_shares += amount  # In this Sacco, 100% of deposits translate to equity shares

        transaction = LedgerTransaction(
            account_id=account.id,
            transaction_type="DEPOSIT",
            amount=amount,
            balance_after=account.total_savings,
            reference_code=reference_code,
            description=description
        )
        self.db.add(transaction)
        self.db.commit()
        self.db.refresh(transaction)
        self.db.refresh(account)
        return transaction

    def get_account_transactions(self, account_id: int, limit: int = 50) -> List[LedgerTransaction]:
        return self.db.query(LedgerTransaction)\
            .filter(LedgerTransaction.account_id == account_id)\
            .order_by(LedgerTransaction.timestamp.desc())\
            .limit(limit).all()
