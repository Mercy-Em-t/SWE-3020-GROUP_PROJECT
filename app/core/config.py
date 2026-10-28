import os

class Settings:
    PROJECT_NAME: str = "Sacco Digital Savings Tracker API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # SQLite default for local zero-dependency development & CI test execution
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./sacco_tracker.db")
    
    # Financial Engine Defaults
    BORROWING_MULTIPLIER: float = 3.0       # 3x total shares
    ANNUAL_INTEREST_RATE: float = 0.12     # 12% annual flat interest
    LATE_PENALTY_RATE: float = 0.05        # 5% monthly late penalty
    GRACE_PERIOD_DAYS: int = 5              # 5-day grace period before delinquency penalty
    
    SECRET_KEY: str = os.getenv("SECRET_KEY", "sacco-dev-secret-key-3020b")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24

settings = Settings()
