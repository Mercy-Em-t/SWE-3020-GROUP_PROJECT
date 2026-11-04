from typing import Optional
from sqlalchemy.orm import Session
from app.repositories.base import BaseRepository
from app.models.entities import Member, SavingsAccount

class MemberRepository(BaseRepository[Member]):
    def __init__(self, db: Session):
        super().__init__(Member, db)

    def get_by_email(self, email: str) -> Optional[Member]:
        return self.db.query(Member).filter(Member.email == email).first()

    def get_by_phone(self, phone: str) -> Optional[Member]:
        return self.db.query(Member).filter(Member.phone_number == phone).first()

    def create_with_account(self, member: Member) -> Member:
        """Atomically create Member and an initial zero-balance SavingsAccount."""
        self.db.add(member)
        self.db.flush()
        account = SavingsAccount(
            member_id=member.id,
            total_shares=0.0,
            total_savings=0.0
        )
        self.db.add(account)
        self.db.commit()
        self.db.refresh(member)
        return member
