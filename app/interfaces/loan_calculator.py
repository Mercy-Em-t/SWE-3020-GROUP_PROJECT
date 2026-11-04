from abc import ABC, abstractmethod
from typing import Dict, Any

class ILoanCalculator(ABC):
    """
    Single Responsibility (SRP) & Interface Segregation (ISP):
    Exclusively specifies pure financial math contracts.
    """
    @abstractmethod
    def calculate_borrowing_limit(self, total_shares: float) -> float:
        """Compute the maximum allowable loan principal based on shares multiplier (3x)."""
        pass

    @abstractmethod
    def calculate_amortization(self, principal: float, annual_rate: float, duration_months: int) -> Dict[str, Any]:
        """Compute monthly installment, total interest, and total repayable amount."""
        pass

    @abstractmethod
    def calculate_delinquency_penalty(self, overdue_balance: float, days_late: int) -> float:
        """Calculate penalty fee if days_late exceeds project grace period."""
        pass
