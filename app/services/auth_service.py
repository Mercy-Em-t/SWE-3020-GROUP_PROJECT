import secrets
from app.repositories.member_repo import MemberRepository
from app.repositories.audit_repo import AuditRepository
from app.models.entities import Member, UserRole
from app.schemas.member import (
    MemberRegisterRequest,
    MemberLoginRequest,
    TokenResponse,
    AdminMemberCreateRequest,
    AdminMemberCreateResponse
)
from app.core.security import hash_password, verify_password, create_access_token


class AuthService:
    def __init__(self, member_repo: MemberRepository, audit_repo: AuditRepository):
        self.member_repo = member_repo
        self.audit_repo = audit_repo

    def _ensure_unique(self, email: str, phone_number: str) -> None:
        if self.member_repo.get_by_email(email):
            raise ValueError(f"Email {email} is already registered.")
        if self.member_repo.get_by_phone(phone_number):
            raise ValueError(f"Phone number {phone_number} is already in use.")

    def register_member(self, request: MemberRegisterRequest) -> Member:
        self._ensure_unique(request.email, request.phone_number)

        # Privilege-escalation guard: public self-registration can never
        # create an admin/treasurer, whatever the client sends in `role`.
        member = Member(
            email=request.email,
            full_name=request.full_name,
            phone_number=request.phone_number,
            role=UserRole.MEMBER.value,
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

    def admin_create_member(
        self, request: AdminMemberCreateRequest, actor_email: str
    ) -> AdminMemberCreateResponse:
        """Admin onboarding: may assign roles; issues a one-time temporary password."""
        digits = "".join(ch for ch in request.phone_number if ch.isdigit())
        email = request.email or f"{digits}@sacco.internal"
        self._ensure_unique(email, request.phone_number)

        temporary_password = secrets.token_urlsafe(9)
        member = Member(
            email=email,
            full_name=request.full_name,
            phone_number=request.phone_number,
            role=request.role,
            hashed_password=hash_password(temporary_password)
        )
        created = self.member_repo.create_with_account(member)

        self.audit_repo.log_event(
            actor_email=actor_email,
            action="MEMBER_ONBOARDED",
            entity_name="Member",
            entity_id=created.id,
            delta=f"Role: {created.role}"
        )
        return AdminMemberCreateResponse(
            id=created.id,
            email=created.email,
            full_name=created.full_name,
            phone_number=created.phone_number,
            role=created.role,
            temporary_password=temporary_password
        )

    def _find_member_by_phone(self, phone: str):
        clean = phone.replace(" ", "").replace("-", "")
        m = self.member_repo.get_by_phone(clean)
        if not m and clean.startswith("0"):
            m = self.member_repo.get_by_phone("+254" + clean[1:])
        elif not m and clean.startswith("+254"):
            m = self.member_repo.get_by_phone("0" + clean[4:])
        return m

    def authenticate_member(self, request: MemberLoginRequest) -> TokenResponse:
        member = None
        if request.email:
            member = self.member_repo.get_by_email(request.email)
        elif request.phone_number:
            member = self._find_member_by_phone(request.phone_number)
            if not member and "@" in request.phone_number:
                member = self.member_repo.get_by_email(request.phone_number)
        elif request.identifier:
            if "@" in request.identifier:
                member = self.member_repo.get_by_email(request.identifier)
            else:
                member = self._find_member_by_phone(request.identifier)
                if not member:
                    member = self.member_repo.get_by_email(request.identifier)

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
            member_id=member.id,
            full_name=member.full_name
        )
