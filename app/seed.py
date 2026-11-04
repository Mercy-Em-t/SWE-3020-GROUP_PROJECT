from datetime import datetime, timedelta, timezone
from app.core.database import SessionLocal, Base, engine
from app.core.security import hash_password
from app.models.entities import Member, SavingsAccount, LedgerTransaction, Loan, GuarantorCommitment, AuditLog

def seed_database():
    """Prime the database with initial demo data for the Wednesday presentation."""
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    # Check if already seeded
    if db.query(Member).first():
        print("Database already contains records. Skipping seed.")
        db.close()
        return

    print("Seeding demo members, savings accounts, and loans...")

    # 1. Admin / Treasurer
    admin = Member(
        email="treasurer@sacco.org",
        full_name="Prof. Eunice (Treasurer Admin)",
        phone_number="+254700111222",
        role="treasurer",
        hashed_password=hash_password("AdminSecure123!")
    )
    db.add(admin)
    db.flush()

    admin_acct = SavingsAccount(member_id=admin.id, total_shares=50000.0, total_savings=50000.0)
    db.add(admin_acct)

    # 2. Active Member / Saver (Mercy)
    member = Member(
        email="mercy@sacco.org",
        full_name="Mercy Emurugat (Saver)",
        phone_number="+254712345678",
        role="member",
        hashed_password=hash_password("MemberPass123!")
    )
    db.add(member)
    db.flush()

    member_acct = SavingsAccount(member_id=member.id, total_shares=25000.0, total_savings=25000.0)
    db.add(member_acct)
    db.flush()

    # Initial Deposit Ledger Entries
    tx1 = LedgerTransaction(
        account_id=member_acct.id,
        transaction_type="DEPOSIT",
        amount=15000.0,
        balance_after=15000.0,
        reference_code="MPESA_SEEDED_001",
        description="Monthly Savings via M-Pesa STK Push"
    )
    tx2 = LedgerTransaction(
        account_id=member_acct.id,
        transaction_type="DEPOSIT",
        amount=10000.0,
        balance_after=25000.0,
        reference_code="MPESA_SEEDED_002",
        description="Additional share capital contribution"
    )
    db.add_all([tx1, tx2])

    # 3. Guarantor Member (Jescah)
    guarantor = Member(
        email="jescah@sacco.org",
        full_name="Jescah Otwoma (Guarantor)",
        phone_number="+254798765432",
        role="member",
        hashed_password=hash_password("GuarantorPass123!")
    )
    db.add(guarantor)
    db.flush()

    guarantor_acct = SavingsAccount(member_id=guarantor.id, total_shares=40000.0, total_savings=40000.0)
    db.add(guarantor_acct)
    db.flush()

    # 4. Active Loan Example
    # Principal KES 45,000. Repayable = 45,000 + (45,000 * 0.12) = 50,400.
    loan = Loan(
        member_id=member.id,
        principal_amount=45000.0,
        interest_rate=0.12,
        duration_months=12,
        total_repayable=50400.0,
        balance_outstanding=50400.0,
        status="APPROVED",
        due_date=datetime.now(timezone.utc) + timedelta(days=365)
    )
    db.add(loan)
    db.flush()

    # Guarantor commitment: Unsecured portion = 45k - 25k = 20k
    commitment = GuarantorCommitment(
        loan_id=loan.id,
        guarantor_member_id=guarantor.id,
        amount_guaranteed=20000.0,
        status="ACCEPTED",
        responded_at=datetime.now(timezone.utc)
    )
    db.add(commitment)

    # 5. Audit Log Entries
    log1 = AuditLog(
        actor_email=admin.email,
        action="SYSTEM_INIT_SEED",
        entity_name="Database",
        delta="Initialized baseline Sacco members and accounts",
        ip_address="127.0.0.1"
    )
    log2 = AuditLog(
        actor_email=member.email,
        action="LOAN_SUBMISSION",
        entity_name="Loan",
        entity_id=loan.id,
        delta="Requested KES 45,000 (Guaranteed by Jescah Otwoma)",
        ip_address="127.0.0.1"
    )
    db.add_all([log1, log2])

    db.commit()
    db.close()
    print("Database successfully seeded with demo accounts!")

if __name__ == "__main__":
    seed_database()
