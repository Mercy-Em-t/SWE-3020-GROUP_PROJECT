import pytest
from app.repositories.member_repo import MemberRepository
from app.repositories.audit_repo import AuditRepository
from app.services.auth_service import AuthService
from app.schemas.member import MemberRegisterRequest, MemberLoginRequest

def test_register_duplicate_email_fails(db_session):
    member_repo = MemberRepository(db_session)
    audit_repo = AuditRepository(db_session)
    auth_service = AuthService(member_repo, audit_repo)

    req1 = MemberRegisterRequest(
        email="test_dup@sacco.test",
        full_name="Duplicate User",
        phone_number="+254711111111",
        password="ValidPassword123"
    )
    auth_service.register_member(req1)

    # Attempt second registration with same email
    req2 = MemberRegisterRequest(
        email="test_dup@sacco.test",
        full_name="Another User",
        phone_number="+254722222222",
        password="ValidPassword123"
    )
    with pytest.raises(ValueError, match="already registered"):
        auth_service.register_member(req2)

def test_authenticate_invalid_credentials_fails(db_session):
    member_repo = MemberRepository(db_session)
    audit_repo = AuditRepository(db_session)
    auth_service = AuthService(member_repo, audit_repo)

    req = MemberRegisterRequest(
        email="login_fail@sacco.test",
        full_name="Login Fail",
        phone_number="+254733333333",
        password="CorrectPassword123"
    )
    auth_service.register_member(req)

    # Wrong password
    with pytest.raises(ValueError, match="Invalid email or password"):
        auth_service.authenticate_member(MemberLoginRequest(
            email="login_fail@sacco.test",
            password="WrongPassword999"
        ))

    # Non-existent user
    with pytest.raises(ValueError, match="Invalid email or password"):
        auth_service.authenticate_member(MemberLoginRequest(
            email="does_not_exist@sacco.test",
            password="AnyPassword"
        ))
