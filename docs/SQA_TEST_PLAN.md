# Software Quality Assurance (SQA) & Test Plan

**System:** Sacco Digital Savings Tracker  
**Course:** SWE3020B – Software Quality Assurance and Security  
**Evaluation Marks Covered:** Testing (3 Marks)  

---

## 1. Testing Strategy & Hierarchy

The project adheres to the **ISO/IEC/IEEE 29119** testing standards and the classical **Testing Pyramid**:

```
            / \
           /   \
          / E2E \       <-- API User Journey Tests (FastAPI TestClient)
         /-------\
        /  Integ  \     <-- Service + Repository + SQLite Database Tests
       /-----------\
      /    Unit     \   <-- PyTest Pure Deterministic Mathematical Tests
     +---------------+
```

### 1.1 Testing Objectives
1. **Financial Precision:** Ensure no floating-point rounding errors or balance drift during loan interest, amortization, and savings accruals.
2. **Defensive Validation:** Prevent invalid deposits (zero or negative amounts) or loans exceeding member qualification limits.
3. **Transaction Atomicity:** Verify that failures during payment or ledger recording trigger clean rollbacks without corrupting member records.
4. **Append-Only Immutability:** Verify that historical ledger records and audit trail logs cannot be modified or truncated.

---

## 2. Test Cases Specification & Traceability Matrix

| Test Case ID | Target Feature / Function | Input Data / Scenario | Expected Outcome | Level |
| :--- | :--- | :--- | :--- | :--- |
| **TC-AUTH-01** | User Registration (`FR-01`) | Valid email, password (hashed), role="member" | 201 Created, user entity persisted with hashed password (never plain text) | Integration |
| **TC-AUTH-02** | User Login & JWT (`FR-01`) | Correct email and password | 200 OK, returns valid JWT token containing role claims | Integration |
| **TC-AUTH-03** | Invalid Login Attempt (`FR-01`) | Incorrect password | 401 Unauthorized, zero sensitive exception details leaked | Integration |
| **TC-SAV-01** | Valid Deposit (`FR-02`, `FR-03`) | Positive amount (KES 5,000), valid phone number | 200 OK, balance increments exactly by KES 5,000, ledger row written | Unit / Integ |
| **TC-SAV-02** | Negative/Zero Deposit (`FR-02`) | Amount = -100 or 0 | 422 Unprocessable Entity, transaction rejected, balance untouched | Unit |
| **TC-LOAN-01** | Borrowing Limit Math (`FR-04`) | Total Shares = KES 10,000 | Max borrowing limit evaluates strictly to KES 30,000 ($3 \times \text{Shares}$) | Unit |
| **TC-LOAN-02** | Loan Within Limit (`FR-05`) | Principal KES 25,000 (Shares = KES 10,000) | Application successfully created with status PENDING | Integration |
| **TC-LOAN-03** | Loan Exceeding Limit (`FR-05`) | Principal KES 35,000 (Shares = KES 10,000) | Validation error raised: Principal exceeds allowable limit | Unit |
| **TC-LOAN-04** | Guarantor Sufficiency (`FR-06`) | Unsecured amount = KES 15,000, Guarantor commits KES 15,000 | Validation passes, loan eligible for approval | Unit |
| **TC-LOAN-05** | Guarantor Shortfall (`FR-06`) | Unsecured amount = KES 15,000, Guarantor commits KES 5,000 | Validation error: Insufficient guarantor coverage | Unit |
| **TC-LOAN-06** | Late Penalty Calculation (`FR-08`) | Days overdue = 35 (Past 5-day grace period), Monthly Rate = 5% | Penalty assessed strictly at $5\% \times \text{Balance}$ | Unit |
| **TC-LEDGER-01** | Append-Only Invariant (`FR-09`) | Post deposit and repayment entries | Historical ledger row IDs and timestamps remain strictly monotonically increasing | Unit |
| **TC-AUDIT-01** | Audit Trail Logging (`FR-10`) | Trigger deposit and loan approval | Audit table logs actor email, action name, target entity ID, and timestamp | Integration |

---

## 3. Automation & Code Coverage Target

* **Test Runner:** **PyTest** (`pytest`)
* **Coverage Target:** $\ge 85\%$ statement and branch coverage across domain and service packages.
* **Continuous Integration:** Automated on every pull request via GitHub Actions (`.github/workflows/backend-ci.yml`).
