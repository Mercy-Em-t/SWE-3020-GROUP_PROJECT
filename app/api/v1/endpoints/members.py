from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas.member import MemberDetailResponse
from app.repositories.member_repo import MemberRepository

router = APIRouter(prefix="/members", tags=["Member Directory"])


@router.get("", response_model=List[MemberDetailResponse])
def list_members(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Retrieve all SACCO members with their savings and shares balance."""
    repo = MemberRepository(db)
    members = repo.list_all(skip=skip, limit=limit)
    result = []
    for m in members:
        savings = m.account.total_savings if m.account else 0.0
        shares = m.account.total_shares if m.account else 0.0
        result.append(
            MemberDetailResponse(
                id=m.id,
                email=m.email,
                full_name=m.full_name,
                phone_number=m.phone_number,
                role=m.role,
                total_savings=savings,
                total_shares=shares,
                created_at=m.created_at
            )
        )
    return result
