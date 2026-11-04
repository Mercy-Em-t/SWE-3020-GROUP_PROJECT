import hashlib
import hmac
import base64
import json
import time
from typing import Dict, Any, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.database import get_db
from app.models.entities import Member, UserRole
from app.repositories.member_repo import MemberRepository

security_scheme = HTTPBearer(auto_error=False)


def hash_password(password: str) -> str:
    """Hash password using SHA-256 with project secret salt."""
    salt = settings.SECRET_KEY.encode('utf-8')
    return hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000).hex()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain-text password against stored PBKDF2 hash."""
    return hmac.compare_digest(hash_password(plain_password), hashed_password)


def create_access_token(data: Dict[str, Any]) -> str:
    """Create a lightweight signed token containing user claims."""
    payload = data.copy()
    payload["exp"] = int(time.time()) + (settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60)
    payload_bytes = json.dumps(payload).encode('utf-8')
    payload_b64 = base64.urlsafe_b64encode(payload_bytes).decode('utf-8')
    signature = hmac.new(settings.SECRET_KEY.encode('utf-8'), payload_b64.encode('utf-8'), hashlib.sha256).hexdigest()
    return f"{payload_b64}.{signature}"


def decode_access_token(token: str) -> Optional[Dict[str, Any]]:
    """Decode and verify the integrity of a signed access token."""
    try:
        parts = token.split(".")
        if len(parts) != 2:
            return None
        payload_b64, signature = parts
        expected_sig = hmac.new(
            settings.SECRET_KEY.encode('utf-8'),
            payload_b64.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        if not hmac.compare_digest(signature, expected_sig):
            return None
        payload_json = base64.urlsafe_b64decode(payload_b64.encode('utf-8')).decode('utf-8')
        payload = json.loads(payload_json)
        if payload.get("exp", 0) < int(time.time()):
            return None  # Expired
        return payload
    except Exception:
        return None


def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security_scheme),
    db: Session = Depends(get_db)
) -> Member:
    """Extract and validate the authenticated user from the Bearer token."""
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication credentials required."
        )
    token = credentials.credentials
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired access token."
        )
    email = payload.get("sub")
    if not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token claims."
        )
    member = MemberRepository(db).get_by_email(email)
    if not member:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authenticated user no longer exists."
        )
    return member


def get_current_admin(
    current_user: Member = Depends(get_current_user)
) -> Member:
    """Require administrator or treasurer role."""
    if current_user.role not in [UserRole.ADMIN.value, UserRole.TREASURER.value]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Administrative privilege required."
        )
    return current_user
