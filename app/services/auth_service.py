from app.repositories.member_repo import MemberRepository
from app.repositories.audit_repo import AuditRepository
from app.models.entities import Member
from app.schemas.member import (
    MemberRegisterRequest,
    MemberLoginRequest,
    TokenResponse
)
from app.core.security import hash_password, verify_password, create_access_token


class AuthService:
    def __init__(self, member_repo: MemberRepository, audit_repo: AuditRepository):
        self.member_repo = member_repo
        self.audit_repo = audit_repo

    def register_member(self, request: MemberRegisterRequest) -> Member:
        if self.member_repo.get_by_email(request.email):
            raise ValueError(f"Email {request.email} is already registered.")
        if self.member_repo.get_by_phone(request.phone_number):
            raise ValueError(f"Phone number {request.phone_number} is already in use.")

        member = Member(
            email=request.email,
            full_name=request.full_name,
            phone_number=request.phone_number,
            role=request.role or "member",
            hashed_password=hash_password(request.password)
        )
        created_member = self.member_repo.create_with_account(member)

        self.audit_repo.log_event(
            actor_email=created_member.email,
            action="MEMBER_REGISTERED",
            entity_name="Member",
            entity_id=created_member.id,
            delta=f"Role: {created_member.role}"
        )
        return created_member

    def authenticate_member(self, request: MemberLoginRequest) -> TokenResponse:
        member = None
        if request.email:
            member = self.member_repo.get_by_email(request.email)
        elif request.phone_number:
            member = self.member_repo.get_by_phone(request.phone_number)
        elif request.identifier:
            member = self.member_repo.get_by_email(request.identifier)
            if not member:
                member = self.member_repo.get_by_phone(request.identifier)

        if not member or not verify_password(request.password, member.hashed_password):
            raise ValueError("Invalid email or password.")

        token = create_access_token({
            "sub": member.email,
            "role": member.role,
            "member_id": member.id
        })

        self.audit_repo.log_event(
            actor_email=member.email,
            action="MEMBER_LOGIN_SUCCESS",
            entity_name="Member",
            entity_id=member.id
        )

        return TokenResponse(
            access_token=token,
            role=member.role,
            email=member.email,
            member_id=member.id
        )
