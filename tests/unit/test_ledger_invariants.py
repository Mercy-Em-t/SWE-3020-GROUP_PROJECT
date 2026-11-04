import pytest
from app.repositories.ledger_repo import LedgerRepository
from app.models.entities import SavingsAccount

def test_ledger_record_deposit_atomicity(db_session):
    """FR-03 & FR-09: Verify atomic balance update and immutable transaction creation."""
    repo = LedgerRepository(db_session)
    account = SavingsAccount(member_id=1, total_shares=1000.0, total_savings=1000.0)
    db_session.add(account)
    db_session.commit()
    db_session.refresh(account)

    # Execute deposit
    tx = repo.record_deposit(
        account_id=account.id,
        amount=5000.0,
        reference_code="TX_TEST_001",
        description="Monthly contribution"
    )

    assert tx.id is not None
    assert tx.amount == 5000.0
    assert tx.balance_after == 6000.0
    assert tx.reference_code == "TX_TEST_001"

    # Verify parent account was updated atomically
    refreshed_account = repo.get_by_id(account.id)
    assert refreshed_account.total_savings == 6000.0
    assert refreshed_account.total_shares == 6000.0

def test_ledger_rejects_missing_account(db_session):
    repo = LedgerRepository(db_session)
    with pytest.raises(ValueError, match="Account with ID 999 not found"):
        repo.record_deposit(account_id=999, amount=500.0, reference_code="TX_FAIL", description="Fail")
