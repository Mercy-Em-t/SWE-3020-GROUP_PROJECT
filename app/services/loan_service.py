from typing import Dict, Any, List
from app.interfaces.loan_calculator import ILoanCalculator
from app.core.config import settings

class LoanCalculationService(ILoanCalculator):
    """
    Single Responsibility Principle (SRP):
    Strictly encapsulates financial math and loan rule algorithms.
    Zero direct coupling to databases or HTTP transport.
    """
    def __init__(
        self,
        multiplier: float = settings.BORROWING_MULTIPLIER,
        default_annual_rate: float = settings.ANNUAL_INTEREST_RATE,
        penalty_rate: float = settings.LATE_PENALTY_RATE,
        grace_period_days: int = settings.GRACE_PERIOD_DAYS
    ):
        self.multiplier = multiplier
        self.default_annual_rate = default_annual_rate
        self.penalty_rate = penalty_rate
        self.grace_period_days = grace_period_days

    def calculate_borrowing_limit(self, total_shares: float) -> float:
        """
        Rule: Maximum borrowing limit = 3x accumulated shares.
        Boundary: If shares <= 0, limit is strictly 0.0.
        """
        if total_shares <= 0.0:
            return 0.0
        return round(total_shares * self.multiplier, 2)

    def calculate_amortization(self, principal: float, annual_rate: float = None, duration_months: int = 12) -> Dict[str, Any]:
        """
        Calculates flat-rate interest and monthly repayment obligation.
        Total Interest = Principal * (annual_rate * (duration_months / 12))
        """
        if principal <= 0:
            raise ValueError("Principal amount must be positive.")
        if duration_months <= 0:
            raise ValueError("Duration in months must be greater than zero.")

        rate = annual_rate if annual_rate is not None else self.default_annual_rate
        total_interest = round(principal * (rate * (duration_months / 12.0)), 2)
        total_repayable = round(principal + total_interest, 2)
        monthly_installment = round(total_repayable / duration_months, 2)

        return {
            "principal": principal,
            "annual_interest_rate": rate,
            "duration_months": duration_months,
            "total_interest": total_interest,
            "total_repayable": total_repayable,
            "monthly_installment": monthly_installment
        }

    def validate_guarantor_coverage(self, principal: float, applicant_shares: float, guarantors: List[Dict[str, float]]) -> bool:
        """
        Financial Rule:
        If Principal > Applicant Shares, the uncollateralized delta MUST be 100%
        covered by total verified guarantor commitments.
        """
        unsecured_delta = max(0.0, principal - applicant_shares)
        if unsecured_delta == 0.0:
            return True  # Fully collateralized by own shares
        
        total_guaranteed = sum(g.get("amount", 0.0) for g in guarantors)
        return total_guaranteed >= unsecured_delta

    def calculate_delinquency_penalty(self, overdue_balance: float, days_late: int) -> float:
        """
        Delinquency Rule:
        If days_late <= grace_period_days, penalty = 0.
        Otherwise, penalty = 5% of the overdue balance.
        """
        if overdue_balance <= 0:
            return 0.0
        if days_late <= self.grace_period_days:
            return 0.0
        return round(overdue_balance * self.penalty_rate, 2)
