# SACCO Digital Savings Tracker: Algorithmic Pseudocode Companion

**Course:** SWE3020B – Software Quality Assurance and Security (USIU-Africa)  
**Deliverable:** CAT 2 System Documentation & Algorithmic Companion  
**Engineering Team:**
* **Mercy Tryphen** – System Architecture & Backend Infrastructure
* **Jescah Otwoma** – API Contracts & Payment Gateways
* **Nyeliep Nial** – Frontend UI/UX Design & Client Architecture
* **Tayak Ruai** – Software Quality Assurance & Test Engineering
* **Roy Githaiga** – Client Integration & Agile Scrum Facilitator  

---

## 1. Purpose of This Document

This document provides a language-agnostic, mathematically rigorous **Pseudocode Companion** for all core Python files (`*.py`) in the backend repository. It translates low-level SQLAlchemy, FastAPI, and Pydantic implementations into high-level algorithmic logic, making it ideal for:
1. **Academic Defense:** Explaining algorithm mechanics directly to examiners without syntax distraction.
2. **Cross-Team Alignment:** Allowing frontend and QA engineers to trace exact backend calculation rules.
3. **Auditing & Security Verification:** Providing a formal specification of cryptographic and financial invariants.

---

## 2. Core Financial & Mathematical Algorithms (`app/services/loan_service.py`)

### Algorithm 1: Dynamic Borrowing Limit Calculation ($3\times$ Multiplier)
* **Source:** [`app/services/loan_service.py`](file:///c:/Users/user/Documents/Quality%20assurance/SWE-3020-GROUP_PROJECT/app/services/loan_service.py#L23)
* **Interface:** [`app/interfaces/loan_calculator.py`](file:///c:/Users/user/Documents/Quality%20assurance/SWE-3020-GROUP_PROJECT/app/interfaces/loan_calculator.py)

```text
ALGORITHM CalculateBorrowingLimit(total_shares: REAL, multiplier: REAL = 3.0) -> REAL
INPUT: 
    total_shares (accumulated share capital of member)
    multiplier (statutory SACCO leverage multiplier, default 3.0)
OUTPUT: 
    Maximum allowable principal borrowing ceiling

BEGIN
    IF total_shares <= 0.0 THEN
        RETURN 0.0
    END IF

    limit <- total_shares * multiplier
    RETURN ROUND(limit, 2)
END
```

---

### Algorithm 2: Flat-Rate Amortization Schedule
* **Source:** [`app/services/loan_service.py`](file:///c:/Users/user/Documents/Quality%20assurance/SWE-3020-GROUP_PROJECT/app/services/loan_service.py#L32)

```text
ALGORITHM CalculateAmortization(principal: REAL, annual_rate: REAL = 0.12, duration_months: INTEGER) -> RECORD
INPUT:
    principal (loan principal requested, > 0)
    annual_rate (flat annual interest rate, default 12% = 0.12)
    duration_months (repayment horizon in months, 1 to 36)
OUTPUT:
    RECORD containing total_interest, total_repayable, monthly_installment

BEGIN
    IF principal <= 0 THEN
        THROW ValueError("Principal amount must be positive.")
    END IF
    IF duration_months <= 0 THEN
        THROW ValueError("Duration in months must be greater than zero.")
    END IF

    // Calculate flat interest across temporal fraction
    temporal_factor <- duration_months / 12.0
    total_interest <- ROUND(principal * (annual_rate * temporal_factor), 2)
    
    total_repayable <- ROUND(principal + total_interest, 2)
    monthly_installment <- ROUND(total_repayable / duration_months, 2)

    RETURN {
        "principal": principal,
        "annual_interest_rate": annual_rate,
        "duration_months": duration_months,
        "total_interest": total_interest,
        "total_repayable": total_repayable,
        "monthly_installment": monthly_installment
    }
END
```

---

### Algorithm 3: Delinquency Penalty with Grace Period
* **Source:** [`app/services/loan_service.py`](file:///c:/Users/user/Documents/Quality%20assurance/SWE-3020-GROUP_PROJECT/app/services/loan_service.py#L69)

```text
ALGORITHM CalculateDelinquencyPenalty(overdue_balance: REAL, days_late: INTEGER, 
                                     grace_period_days: INTEGER = 5, penalty_rate: REAL = 0.05) -> REAL
INPUT:
    overdue_balance (unpaid balance past maturity date)
    days_late (number of calendar days since due date)
    grace_period_days (threshold before penalty applies, default 5)
    penalty_rate (flat penalty surcharge, default 5% = 0.05)
OUTPUT:
    Assessed penalty surcharge

BEGIN
    IF overdue_balance <= 0.0 THEN
        RETURN 0.0
    END IF

    // Invariant: Within grace period, penalty is strictly waived
    IF days_late <= grace_period_days THEN
        RETURN 0.0
    END IF

    penalty <- overdue_balance * penalty_rate
    RETURN ROUND(penalty, 2)
END
```

---

### Algorithm 4: Multi-Guarantor Collateral Sufficiency Verification
* **Source:** [`app/services/loan_service.py`](file:///c:/Users/user/Documents/Quality%20assurance/SWE-3020-GROUP_PROJECT/app/services/loan_service.py#L56)

```text
ALGORITHM ValidateGuarantorCoverage(principal: REAL, applicant_shares: REAL, 
                                   guarantors: LIST OF RECORD) -> BOOLEAN
INPUT:
    principal (requested loan amount)
    applicant_shares (borrower's own accumulated savings)
    guarantors (list of {guarantor_id, amount} commitments)
OUTPUT:
    TRUE if loan is 100% collateralized, FALSE otherwise

BEGIN
    unsecured_delta <- MAX(0.0, principal - applicant_shares)

    // If borrower's own shares fully cover principal, no guarantor is mandatory
    IF unsecured_delta == 0.0 THEN
        RETURN TRUE
    END IF

    total_guaranteed <- 0.0
    FOR EACH g IN guarantors DO
        total_guaranteed <- total_guaranteed + g.amount
    END FOR

    RETURN total_guaranteed >= unsecured_delta
END
```

---

## 3. Cryptographic & Security Subsystems (`app/core/security.py`)

### Algorithm 5: Password Hashing (PBKDF2-HMAC-SHA256)
* **Source:** [`app/core/security.py`](file:///c:/Users/user/Documents/Quality%20assurance/SWE-3020-GROUP_PROJECT/app/core/security.py#L18)

```text
ALGORITHM HashPassword(plain_password: STRING, secret_key: STRING) -> HEX_STRING
INPUT:
    plain_password (raw user password string)
    secret_key (high-entropy server secret)
OUTPUT:
    Salted, iterated hex digest conforming to OWASP ASVS

BEGIN
    salt <- UTF8_ENCODE(secret_key)
    iterations <- 100000
    digest <- PBKDF2_HMAC(hash_function="sha256", 
                          password=UTF8_ENCODE(plain_password), 
                          salt=salt, 
                          iterations=iterations)
    RETURN HEX_ENCODE(digest)
END
```

---

### Algorithm 6: Constant-Time Password Verification
* **Source:** [`app/core/security.py`](file:///c:/Users/user/Documents/Quality%20assurance/SWE-3020-GROUP_PROJECT/app/core/security.py#L24)

```text
ALGORITHM VerifyPassword(plain_password: STRING, stored_hash: STRING, secret_key: STRING) -> BOOLEAN
INPUT:
    plain_password (candidate plaintext from login form)
    stored_hash (hex hash from members database table)
OUTPUT:
    TRUE if matched, FALSE otherwise (timing-attack resistant)

BEGIN
    candidate_hash <- HashPassword(plain_password, secret_key)
    // Invariant: Constant-time comparison prevents side-channel timing attacks
    RETURN CONSTANT_TIME_COMPARE(candidate_hash, stored_hash)
END
```

---

### Algorithm 7: Signed JWT Token Issuance & Validation
* **Source:** [`app/core/security.py`](file:///c:/Users/user/Documents/Quality%20assurance/SWE-3020-GROUP_PROJECT/app/core/security.py#L29)

```text
ALGORITHM CreateAccessToken(claims: DICTIONARY, secret_key: STRING, expire_minutes: INTEGER = 60) -> STRING
BEGIN
    payload <- COPY(claims)
    payload["exp"] <- CURRENT_UNIX_TIMESTAMP() + (expire_minutes * 60)
    
    payload_json <- JSON_SERIALIZE(payload)
    payload_b64 <- BASE64_URL_ENCODE(payload_json)
    
    signature <- HMAC_SHA256(key=secret_key, message=payload_b64)
    RETURN CONCATENATE(payload_b64, ".", signature)
END

ALGORITHM DecodeAccessToken(token: STRING, secret_key: STRING) -> OPTIONAL DICTIONARY
BEGIN
    parts <- SPLIT(token, by=".")
    IF LENGTH(parts) != 2 THEN
        RETURN NULL
    END IF

    payload_b64 <- parts[0]
    provided_signature <- parts[1]

    expected_signature <- HMAC_SHA256(key=secret_key, message=payload_b64)
    IF NOT CONSTANT_TIME_COMPARE(provided_signature, expected_signature) THEN
        RETURN NULL  // Tampered token
    END IF

    payload <- JSON_DESERIALIZE(BASE64_URL_DECODE(payload_b64))
    IF payload["exp"] < CURRENT_UNIX_TIMESTAMP() THEN
        RETURN NULL  // Expired token
    END IF

    RETURN payload
END
```

---

## 4. Double-Entry Ledger & Transactional Services (`app/services/savings_service.py`)

### Algorithm 8: Inbound Deposit Processing with Ledger Invariance
* **Source:** [`app/services/savings_service.py`](file:///c:/Users/user/Documents/Quality%20assurance/SWE-3020-GROUP_PROJECT/app/services/savings_service.py#L20)
* **Repositories:** [`LedgerRepository`](file:///c:/Users/user/Documents/Quality%20assurance/SWE-3020-GROUP_PROJECT/app/repositories/ledger_repo.py), [`AuditRepository`](file:///c:/Users/user/Documents/Quality%20assurance/SWE-3020-GROUP_PROJECT/app/repositories/audit_repo.py)

```text
ALGORITHM ProcessDeposit(request: DepositRequest, payment_gateway: IPaymentGateway, 
                         ledger_repo: LedgerRepository, audit_repo: AuditRepository) -> DepositResponse
INPUT:
    request (contains member_id, amount, phone_number, channel)
OUTPUT:
    Deposit confirmation with updated balance

BEGIN
    // Step 1: Validate Account Existence
    account <- ledger_repo.GetByMemberId(request.member_id)
    IF account IS NULL THEN
        THROW ValueError("Savings account not found.")
    END IF

    // Step 2: Generate Idempotency Reference
    reference <- "DAR_" + GENERATE_RANDOM_HEX(8)

    // Step 3: Trigger Payment Gateway Adapter (M-Pesa STK Push / Bank Wire)
    payment_result <- AWAIT payment_gateway.InitiateDeposit(
        phone_number=request.phone_number,
        amount=request.amount,
        reference=reference
    )

    IF payment_result.success IS FALSE THEN
        THROW Exception("Payment gateway rejected transaction: " + payment_result.message)
    END IF

    // Step 4: Atomic Double-Entry Ledger Commit (Invariance: New Bal = Old Bal + Delta)
    new_savings_balance <- account.total_savings + request.amount
    new_total_shares <- account.total_shares + request.amount

    // Append-only write to ledger_transactions table
    transaction_record <- {
        "account_id": account.id,
        "transaction_type": "DEPOSIT",
        "amount": request.amount,
        "balance_after": new_savings_balance,
        "reference_code": reference,
        "description": "Inbound deposit via " + request.channel,
        "timestamp": UTC_NOW()
    }
    ledger_repo.RecordTransaction(transaction_record)

    // Mutate parent aggregate balance
    account.total_savings <- new_savings_balance
    account.total_shares <- new_total_shares
    ledger_repo.Commit()

    // Step 5: Append to Forensic Audit Trail
    audit_repo.LogEvent(
        actor_email="system",
        action="DEPOSIT_COMPLETED",
        entity_name="SavingsAccount",
        entity_id=account.id,
        delta="Amount: KES " + STRING(request.amount) + ", New Balance: KES " + STRING(new_savings_balance)
    )

    RETURN DepositResponse(
        success=TRUE,
        new_savings_balance=new_savings_balance,
        new_total_shares=new_total_shares,
        reference_code=reference,
        message="Deposit processed successfully."
    )
END
```

---

## 5. Administrative Vetting & Loan Repayment (`app/api/v1/endpoints/loans.py`)

### Algorithm 9: Two-Stage Loan Vetting & Audit Logging
* **Source:** [`app/api/v1/endpoints/loans.py`](file:///c:/Users/user/Documents/Quality%20assurance/SWE-3020-GROUP_PROJECT/app/api/v1/endpoints/loans.py#L125)

```text
ALGORITHM VetLoanApplication(loan_id: INTEGER, decision: LoanVettingDecision, 
                             loan_repo: LoanRepository, audit_repo: AuditRepository) -> LoanRecord
INPUT:
    loan_id (identifier of pending loan)
    decision (RECORD with status in {"APPROVED", "REJECTED"}, review_notes: STRING)
OUTPUT:
    Updated Loan record

BEGIN
    loan <- loan_repo.GetById(loan_id)
    IF loan IS NULL THEN
        THROW HTTPException(404, "Loan not found.")
    END IF

    IF loan.status != "PENDING" THEN
        THROW HTTPException(400, "Loan has already been adjudicated.")
    END IF

    // Execute state transition
    loan.status <- decision.status
    loan_repo.Commit()

    // Log immutable audit entry
    audit_repo.LogEvent(
        actor_email="admin@sacco.test",
        action="LOAN_" + decision.status,
        entity_name="Loan",
        entity_id=loan_id,
        delta="Decision: " + decision.status + ". Notes: " + decision.review_notes
    )

    RETURN loan
END
```

---

### Algorithm 10: Atomic Loan Repayment & Auto-Closure
* **Source:** [`app/api/v1/endpoints/loans.py`](file:///c:/Users/user/Documents/Quality%20assurance/SWE-3020-GROUP_PROJECT/app/api/v1/endpoints/loans.py#L145)

```text
ALGORITHM ApplyLoanRepayment(request: LoanRepaymentRequest, loan_repo: LoanRepository, 
                             audit_repo: AuditRepository) -> LoanRecord
INPUT:
    request (contains loan_id, amount, payment_reference)
OUTPUT:
    Updated Loan record with adjusted balance

BEGIN
    loan <- loan_repo.GetById(request.loan_id)
    IF loan IS NULL THEN
        THROW HTTPException(404, "Loan record not found.")
    END IF

    // Calculate reduction with non-negativity constraint
    new_balance <- MAX(0.0, loan.balance_outstanding - request.amount)
    loan.balance_outstanding <- new_balance

    // Invariant: Balance reaching 0.0 transitions loan to CLOSED
    IF new_balance == 0.0 THEN
        loan.status <- "CLOSED"
    END IF

    loan_repo.Commit()

    // Record forensic audit entry
    audit_repo.LogEvent(
        actor_email="system",
        action="LOAN_REPAYMENT_APPLIED",
        entity_name="Loan",
        entity_id=loan.id,
        delta="Paid: KES " + STRING(request.amount) + ", Remaining: KES " + STRING(new_balance)
    )

    RETURN loan
END
```

---

## 6. Authentication & Flexible Credential Resolver (`app/services/auth_service.py`)

### Algorithm 11: Multi-Format Identifier Login Resolution
* **Source:** [`app/services/auth_service.py`](file:///c:/Users/user/Documents/Quality%20assurance/SWE-3020-GROUP_PROJECT/app/services/auth_service.py#L42)

```text
ALGORITHM AuthenticateMember(request: MemberLoginRequest, member_repo: MemberRepository) -> TokenResponse
INPUT:
    request (candidate credentials containing password and optional email, phone, or identifier)
OUTPUT:
    TokenResponse with JWT access token, role, and member ID

BEGIN
    candidate_user <- NULL

    // 1. Direct Email Match
    IF request.email IS NOT NULL THEN
        candidate_user <- member_repo.GetByEmail(request.email)

    // 2. Phone Match with Whitespace & Country Code Normalization
    ELSE IF request.phone_number IS NOT NULL THEN
        clean_phone <- STRIP_WHITESPACE(request.phone_number)
        candidate_user <- member_repo.GetByPhone(clean_phone)
        
        // Kenyan format fallback: 07XX... <-> +2547XX...
        IF candidate_user IS NULL AND clean_phone STARTS_WITH "0" THEN
            candidate_user <- member_repo.GetByPhone("+254" + SUBSTRING(clean_phone, 1))
        ELSE IF candidate_user IS NULL AND clean_phone STARTS_WITH "+254" THEN
            candidate_user <- member_repo.GetByPhone("0" + SUBSTRING(clean_phone, 4))
        END IF

        // If email was entered into phone field
        IF candidate_user IS NULL AND "@" IN request.phone_number THEN
            candidate_user <- member_repo.GetByEmail(request.phone_number)
        END IF

    // 3. Generic Identifier Resolver
    ELSE IF request.identifier IS NOT NULL THEN
        IF "@" IN request.identifier THEN
            candidate_user <- member_repo.GetByEmail(request.identifier)
        ELSE
            candidate_user <- FindMemberByPhone(request.identifier)
        END IF
    END IF

    // Verify presence and password cryptographic hash
    IF candidate_user IS NULL OR NOT VerifyPassword(request.password, candidate_user.hashed_password) THEN
        THROW ValueError("Invalid email or password.")
    END IF

    // Generate signed JWT bearer token
    token <- CreateAccessToken({
        "sub": candidate_user.email,
        "role": candidate_user.role,
        "member_id": candidate_user.id
    })

    RETURN TokenResponse(
        access_token=token,
        role=candidate_user.role,
        email=candidate_user.email,
        member_id=candidate_user.id
    )
END
```

---

## 7. Master Traceability: Pseudocode to Python Files

| Pseudocode Algorithm | Concrete Python Implementation | Layer |
| :--- | :--- | :--- |
| **Alg 1: Borrowing Limit ($3\times$)** | [`app/services/loan_service.py`](file:///c:/Users/user/Documents/Quality%20assurance/SWE-3020-GROUP_PROJECT/app/services/loan_service.py#L23) | Domain Service |
| **Alg 2: Flat Amortization** | [`app/services/loan_service.py`](file:///c:/Users/user/Documents/Quality%20assurance/SWE-3020-GROUP_PROJECT/app/services/loan_service.py#L32) | Domain Service |
| **Alg 3: Delinquency Penalty** | [`app/services/loan_service.py`](file:///c:/Users/user/Documents/Quality%20assurance/SWE-3020-GROUP_PROJECT/app/services/loan_service.py#L69) | Domain Service |
| **Alg 4: Guarantor Sufficiency** | [`app/services/loan_service.py`](file:///c:/Users/user/Documents/Quality%20assurance/SWE-3020-GROUP_PROJECT/app/services/loan_service.py#L56) | Domain Service |
| **Alg 5: PBKDF2 Password Hash** | [`app/core/security.py`](file:///c:/Users/user/Documents/Quality%20assurance/SWE-3020-GROUP_PROJECT/app/core/security.py#L18) | Core Security |
| **Alg 6: Constant-Time Verify** | [`app/core/security.py`](file:///c:/Users/user/Documents/Quality%20assurance/SWE-3020-GROUP_PROJECT/app/core/security.py#L24) | Core Security |
| **Alg 7: Signed JWT Issuance** | [`app/core/security.py`](file:///c:/Users/user/Documents/Quality%20assurance/SWE-3020-GROUP_PROJECT/app/core/security.py#L29) | Core Security |
| **Alg 8: Double-Entry Deposit** | [`app/services/savings_service.py`](file:///c:/Users/user/Documents/Quality%20assurance/SWE-3020-GROUP_PROJECT/app/services/savings_service.py#L20) | Domain Service |
| **Alg 9: Two-Stage Loan Vetting** | [`app/api/v1/endpoints/loans.py`](file:///c:/Users/user/Documents/Quality%20assurance/SWE-3020-GROUP_PROJECT/app/api/v1/endpoints/loans.py#L125) | API Router |
| **Alg 10: Loan Repayment** | [`app/api/v1/endpoints/loans.py`](file:///c:/Users/user/Documents/Quality%20assurance/SWE-3020-GROUP_PROJECT/app/api/v1/endpoints/loans.py#L145) | API Router |
| **Alg 11: Multi-Format Auth** | [`app/services/auth_service.py`](file:///c:/Users/user/Documents/Quality%20assurance/SWE-3020-GROUP_PROJECT/app/services/auth_service.py#L42) | Domain Service |
