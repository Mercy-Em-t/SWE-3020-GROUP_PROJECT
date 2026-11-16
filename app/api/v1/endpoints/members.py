from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.security import get_current_user, get_current_admin
from app.models.entities import Member
from app.schemas.member import (
    MemberDetailResponse,
    MemberDirectoryEntry,
    AdminMemberCreateRequest,
    AdminMemberCreateResponse
)
from app.repositories.member_repo import MemberRepository
from app.repositories.audit_repo import AuditRepository
from app.services.auth_service import AuthService

router = APIRouter(prefix="/members", tags=["Member Directory"])


@router.get("", response_model=List[MemberDetailResponse])
def list_members(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    _admin: Member = Depends(get_current_admin)
):
    """[Admin] Retrieve all SACCO members with their savings and shares balance."""
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


@router.get("/directory", response_model=List[MemberDirectoryEntry])
def member_directory(
    db: Session = Depends(get_db),
    _user: Member = Depends(get_current_user)
):
    """[Any member] Names only (no balances or contacts), used to pick loan guarantors."""
    members = MemberRepository(db).list_all(skip=0, limit=1000)
    return [MemberDirectoryEntry(id=m.id, full_name=m.full_name) for m in members]


@router.post(
    "",
    response_model=AdminMemberCreateResponse,
    status_code=status.HTTP_201_CREATED
)
def create_member(
    request: AdminMemberCreateRequest,
    db: Session = Depends(get_db),
    admin: Member = Depends(get_current_admin)
):
    """[Admin] Onboard a member and assign a role; returns a one-time temporary password."""
    service = AuthService(member_repo=MemberRepository(db), audit_repo=AuditRepository(db))
    try:
        return service.admin_create_member(request, actor_email=admin.email)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
