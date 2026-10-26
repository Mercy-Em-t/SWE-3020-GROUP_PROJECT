from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.member import MemberRegisterRequest, MemberLoginRequest, TokenResponse, MemberResponse
from app.repositories.member_repo import MemberRepository
from app.repositories.audit_repo import AuditRepository
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Identity & Access Management"])

def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    return AuthService(
        member_repo=MemberRepository(db),
        audit_repo=AuditRepository(db)
    )

@router.post("/register", response_model=MemberResponse, status_code=status.HTTP_201_CREATED)
def register(request: MemberRegisterRequest, service: AuthService = Depends(get_auth_service)):
    try:
        return service.register_member(request)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post("/login", response_model=TokenResponse)
def login(request: MemberLoginRequest, service: AuthService = Depends(get_auth_service)):
    try:
        return service.authenticate_member(request)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
