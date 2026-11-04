from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
import enum
from app.core.database import Base

def utc_now():
    return datetime.now(timezone.utc)

class UserRole(str, enum.Enum):
    MEMBER = "member"
    TREASURER = "treasurer"
    ADMIN = "admin"

class TransactionType(str, enum.Enum):
    DEPOSIT = "DEPOSIT"
    LOAN_DISBURSEMENT = "LOAN_DISBURSEMENT"
    LOAN_REPAYMENT = "LOAN_REPAYMENT"
    PENALTY = "PENALTY"

class LoanStatus(str, enum.Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    DISBURSED = "DISBURSED"
    CLOSED = "CLOSED"

class GuarantorStatus(str, enum.Enum):
    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"
    DECLINED = "DECLINED"

class Member(Base):
    __tablename__ = "members"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(120), unique=True, index=True, nullable=False)
    full_name = Column(String(150), nullable=False)
    phone_number = Column(String(20), unique=True, index=True, nullable=False)
    role = Column(String(20), default=UserRole.MEMBER.value, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=utc_now)

    account = relationship("SavingsAccount", back_populates="member", uselist=False)
    loans = relationship("Loan", back_populates="borrower")

class SavingsAccount(Base):
    __tablename__ = "savings_accounts"

    id = Column(Integer, primary_key=True, index=True)
    member_id = Column(Integer, ForeignKey("members.id"), unique=True, nullable=False)
    total_shares = Column(Float, default=0.0, nullable=False)
    total_savings = Column(Float, default=0.0, nullable=False)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now)

    member = relationship("Member", back_populates="account")
    transactions = relationship("LedgerTransaction", back_populates="account")

class LedgerTransaction(Base):
    __tablename__ = "ledger_transactions"

    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("savings_accounts.id"), nullable=False)
    transaction_type = Column(String(30), nullable=False)
    amount = Column(Float, nullable=False)
    balance_after = Column(Float, nullable=False)
    reference_code = Column(String(60), unique=True, index=True, nullable=False)
    description = Column(String(255), nullable=True)
    timestamp = Column(DateTime, default=utc_now, nullable=False)

    account = relationship("SavingsAccount", back_populates="transactions")

class Loan(Base):
    __tablename__ = "loans"

    id = Column(Integer, primary_key=True, index=True)
    member_id = Column(Integer, ForeignKey("members.id"), nullable=False)
    principal_amount = Column(Float, nullable=False)
    interest_rate = Column(Float, nullable=False)
    duration_months = Column(Integer, nullable=False)
    total_repayable = Column(Float, nullable=False)
    balance_outstanding = Column(Float, nullable=False)
    penalty_accumulated = Column(Float, default=0.0, nullable=False)
    status = Column(String(20), default=LoanStatus.PENDING.value, nullable=False)
    created_at = Column(DateTime, default=utc_now)
    due_date = Column(DateTime, nullable=False)

    borrower = relationship("Member", back_populates="loans")
    guarantors = relationship("GuarantorCommitment", back_populates="loan")

class GuarantorCommitment(Base):
    __tablename__ = "guarantor_commitments"

    id = Column(Integer, primary_key=True, index=True)
    loan_id = Column(Integer, ForeignKey("loans.id"), nullable=False)
    guarantor_member_id = Column(Integer, ForeignKey("members.id"), nullable=False)
    amount_guaranteed = Column(Float, nullable=False)
    status = Column(String(20), default=GuarantorStatus.PENDING.value, nullable=False)
    responded_at = Column(DateTime, nullable=True)

    loan = relationship("Loan", back_populates="guarantors")
    guarantor = relationship("Member")

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    actor_email = Column(String(120), nullable=False)
    action = Column(String(80), nullable=False)
    entity_name = Column(String(80), nullable=False)
    entity_id = Column(Integer, nullable=True)
    delta = Column(Text, nullable=True)
    ip_address = Column(String(45), default="127.0.0.1")
    timestamp = Column(DateTime, default=utc_now, nullable=False)
