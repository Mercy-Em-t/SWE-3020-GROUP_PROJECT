import pytest
from app.services.loan_service import LoanCalculationService

@pytest.fixture
def calculator():
    return LoanCalculationService(
        multiplier=3.0,
        default_annual_rate=0.12,
        penalty_rate=0.05,
        grace_period_days=5
    )

def test_borrowing_limit_proportional_to_shares(calculator):
    """FR-04: Limit = 3x Shares."""
    assert calculator.calculate_borrowing_limit(10000.0) == 30000.0
    assert calculator.calculate_borrowing_limit(25000.50) == 75001.50

def test_borrowing_limit_zero_or_negative_shares(calculator):
    """FR-04: Zero or negative shares must yield zero borrowing limit."""
    assert calculator.calculate_borrowing_limit(0.0) == 0.0
    assert calculator.calculate_borrowing_limit(-500.0) == 0.0

def test_amortization_calculation(calculator):
    """FR-07: Verify flat-rate interest and monthly installments."""
    # KES 12,000 for 12 months at 12% annual flat
    # Interest = 12000 * 0.12 = 1440
    # Total = 13440
    # Monthly = 1120
    res = calculator.calculate_amortization(principal=12000.0, annual_rate=0.12, duration_months=12)
    assert res["principal"] == 12000.0
    assert res["total_interest"] == 1440.0
    assert res["total_repayable"] == 13440.0
    assert res["monthly_installment"] == 1120.0

def test_amortization_invalid_inputs(calculator):
    with pytest.raises(ValueError, match="Principal amount must be positive"):
        calculator.calculate_amortization(principal=-100.0)

    with pytest.raises(ValueError, match="Duration in months must be greater than zero"):
        calculator.calculate_amortization(principal=1000.0, duration_months=0)

def test_guarantor_coverage_sufficient(calculator):
    """FR-06: Uncollateralized delta must be covered by guarantors."""
    # Principal: 50,000. Own shares: 20,000. Unsecured delta = 30,000.
    guarantors = [
        {"amount": 15000.0},
        {"amount": 15000.0}
    ]
    assert calculator.validate_guarantor_coverage(50000.0, 20000.0, guarantors) is True

def test_guarantor_coverage_shortfall(calculator):
    """FR-06: Reject if guarantors commit less than unsecured delta."""
    # Principal: 50,000. Own shares: 20,000. Unsecured delta = 30,000.
    guarantors = [
        {"amount": 10000.0},
        {"amount": 10000.0}
    ]
    assert calculator.validate_guarantor_coverage(50000.0, 20000.0, guarantors) is False

def test_guarantor_not_needed_if_fully_backed(calculator):
    """FR-06: If own shares cover principal, no guarantor needed."""
    assert calculator.validate_guarantor_coverage(20000.0, 25000.0, []) is True

def test_delinquency_penalty_within_grace_period(calculator):
    """FR-08: Within 5-day grace period, penalty must be zero."""
    assert calculator.calculate_delinquency_penalty(overdue_balance=10000.0, days_late=3) == 0.0
    assert calculator.calculate_delinquency_penalty(overdue_balance=10000.0, days_late=5) == 0.0

def test_delinquency_penalty_past_grace_period(calculator):
    """FR-08: Beyond grace period, apply 5% penalty."""
    # 5% of 10,000 = 500
    assert calculator.calculate_delinquency_penalty(overdue_balance=10000.0, days_late=6) == 500.0
    assert calculator.calculate_delinquency_penalty(overdue_balance=25000.0, days_late=30) == 1250.0
