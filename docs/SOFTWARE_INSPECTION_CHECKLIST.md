# Sacco Digital Savings Tracker — Formal Software Inspection Checklist

**Course:** SWE3020B — Software Quality Assurance and Security  
**Institution:** United States International University - Africa (USIU-Africa)  
**Instructor:** Prof. Eunice Mwangi  
**Governing Standards:** IEEE 1028-2008 (*Standard for Software Reviews and Audits*), ISO/IEC 25010:2023  
**Theoretical Foundation:** Ian Sommerville, *Software Engineering* (Chapter 24: Quality Management — Program Inspection Checklists)  
**Project System:** Sacco Digital Savings Tracker (FastAPI / SQLAlchemy / SQLite Backend & React / Vite Frontend)

---

## 1. Inspection Framework & Governance (IEEE 1028-2008)

Software inspections are a rigorous, formal static verification technique designed to identify defects, design violations, and security vulnerabilities before execution or testing.

### 1.1 Team Inspection Roles
* **Moderator / Inspection Leader:** Facilitates the inspection meeting, ensures adherence to the checklist, prevents personal critiques, and determines gate clearance.
* **Author / Developer:** Originator of the code or artifact; provides architectural context and clarifies intent when asked, but does not defend defective syntax.
* **Inspectors / Reviewers (Peer QA Engineers):** Independently scrutinize the code line-by-line prior to the meeting using this standardized checklist to detect faults.
* **Scribe / Recorder:** Formally records each defect, its classification, severity, exact source location, and remediation deadline in the Defect Register.

### 1.2 Inspection Stage Gate Criteria
* **Entry Criteria:**
  1. Code compiles and passes static linting (`flake8`, `eslint`) with zero syntax errors.
  2. Code accompanied by documented requirements/user story (CRVM properties).
  3. All reviewers have received source files at least 24 hours prior to the inspection session.
* **Exit Criteria:**
  1. 100% of detected Critical and High-severity defects are remediated and re-verified.
  2. Convergence Index ($\text{CI} \ge 0.90$) achieved.
  3. Formal Inspection Record signed off by Moderator and Lead Architect.

---

## 2. Core Program Inspection Checklist (Sommerville Fault Classes)

The checklist operationalizes the 6 canonical fault classes defined by Ian Sommerville, tailored directly to the Python/FastAPI backend and React frontend of the **Sacco Digital Savings Tracker**.

### Table 1: Canonical Fault Classes & Sacco Tracker Inspection Checks

| Fault Class | Sommerville Textbook Inspection Check | Sacco Digital Savings Tracker Contextual Check (Python/FastAPI & React) | Inspection Focus & Risk Target |
| :--- | :--- | :--- | :--- |
| **Data Faults** | • Are all program variables initialized before their values are used?<br>• Have all constants been named?<br>• Should the upper bound of arrays be equal to the size of the array or `Size - 1`?<br>• If character strings are used, is a delimiter explicitly assigned?<br>• Is there any possibility of buffer overflow? | 1. **Financial Precision:** Are money amounts (`deposit`, `loan_balance`, `penalty`) typed as `Decimal` or scaled integers rather than floating-point `float`?<br>2. **State Initialization:** Are React hooks (`useState`, `useMemo`) initialized with safe defaults (e.g. `useState([])`, `useState(null)`) to prevent `TypeError: undefined is not an object`?<br>3. **Business Constants:** Are loan multipliers (e.g. `MAX_LOAN_SAVINGS_MULTIPLIER = 3.0`), grace periods, and late fee percentages defined in `core/config.py` rather than hardcoded magic numbers?<br>4. **Array & List Bounds:** Are list index operations protected against `IndexError` when parsing M-Pesa Daraja callback arrays or statement tables? | Prevents floating-point ledger rounding errors, uninitialized state crashes, and index out-of-range exceptions. |
| **Control Faults** | • For each conditional statement, is the condition correct?<br>• Is each loop certain to terminate?<br>• Are compound statements correctly bracketed?<br>• In case statements, are all possible cases accounted for?<br>• If a `break` is required after each case in case statements, has it been included? | 1. **Eligibility Predicates:** Does loan eligibility strictly evaluate `requested_amount <= (accumulated_shares * 3.0)` and `guarantor_count >= 2` without off-by-one or inverted logic?<br>2. **Authorization Guards:** In route guards (`ProtectedRoute.jsx`), are both `!user` and `user.role !== required_role` evaluated with early returns?<br>3. **Loop Termination:** Do pagination loops or amortization schedule generators have explicit exit bounds and cycle guards?<br>4. **Pattern Matching / Switch Completeness:** Do loan status handlers exhaustively cover all states (`SUBMITTED`, `GUARANTOR_APPROVED`, `TREASURER_APPROVED`, `DISBURSED`, `REJECTED`, `DEFAULTED`) with a fallback default branch? | Eliminates infinite loops in statement generation, bypass of loan thresholds, and unhandled business states. |
| **Input/Output (I/O) Faults** | • Are all input variables used?<br>• Are all output variables assigned a value before they are output?<br>• Can unexpected inputs cause corruption? | 1. **Boundary Schema Validation:** Does every API endpoint validate incoming JSON payloads with Pydantic (`DepositRequest`, `LoanApplicationCreate`) restricting negative amounts, injection strings, and invalid telephone formats?<br>2. **Sanitized Financial Responses:** Do response DTOs (`schemas/loan.py`) omit internal password hashes, system salts, and raw gateway secret keys?<br>3. **Form Submissions:** In React forms, are input fields trimmed and numeric fields sanitized before API dispatch? | Guarantees zero negative deposits/loans, prevents database corruption from unexpected payloads, and blocks credential leakage. |
| **Interface Faults** | • Do all function and method calls have the correct number of parameters?<br>• Do formal and actual parameter types match?<br>• Are the parameters in the right order?<br>• If components access shared memory, do they have the same model of the shared memory structure? | 1. **Component Prop Contracts:** Do React components (e.g., `ProtectedRoute`, `LoanCard`) receive and destructure all required props (e.g., `role`, `children`, `loanData`) without lexical reference errors?<br>2. **Service Parameter Order:** In `LoanCalculationService.calculate_amortization(principal, rate, tenor_months)`, are arguments strictly typed and passed in identical sequence across caller repositories?<br>3. **Dependency Injection:** Are FastAPI dependencies (`db: Session = Depends(get_db)`, `current_user: User = Depends(get_current_active_user)`) correctly resolved in method signatures? | Prevents runtime `ReferenceError`, signature mismatches between API controllers and domain services, and broken DI wiring. |
| **Storage Management Faults** | • If a linked structure is modified, have all links been correctly reassigned?<br>• If dynamic storage is used, has space been allocated correctly?<br>• Is space explicitly deallocated after it is no longer required? | 1. **ORM Session Leaks:** Are SQLAlchemy database sessions managed via context managers (`with SessionLocal() as db:` or FastAPI `yield get_db`) ensuring `db.close()` on all execution paths?<br>2. **Connection Pool Depletion:** Are database connections and file descriptors released, preventing connection exhaustion under concurrent chama member access?<br>3. **Client-Side Storage Sanitization:** Does `localStorage.removeItem("token")` fire completely on logout without lingering JWT remnants? | Eliminates database thread/pool locking, SQLite database locks, and memory leaks on long-running worker processes. |
| **Exception Management Faults** | • Have all possible error conditions been taken into account? | 1. **M-Pesa Webhook Failures:** Are external network timeouts, HTTP 500s, and unparseable callback payloads caught and directed to idempotency logs instead of unhandled 500 crashes?<br>2. **Database Rollbacks:** Does every transactional write block execute `db.rollback()` within an `except Exception:` block prior to re-raising or returning error JSON?<br>3. **Client Error Boundaries:** Does the React app encapsulate async API calls in `try/catch` blocks with user-friendly toast alerts rather than unhandled promise rejections? | Prevents partial database writes, unhandled runtime crashes, and catastrophic silent financial reconciliation failures. |

---

## 3. Database Faults Formal Inspection Table (ID, Fault Class, Check, Result)

| ID | Fault Class | Inspection Check | Result |
| :--- | :--- | :--- | :--- |
| **CHK-DB-01** | **Data Fault (Precision)** | Are monetary amounts (savings, shares, loans, penalties) stored using fixed-point decimals (`Numeric(12, 2)` / `Decimal`) rather than IEEE 754 floating point? | **REMEDIATED**<br>Found `Float` in [`entities.py`](file:///c:/Users/user/Documents/Quality%20assurance/SWE-3020-GROUP_PROJECT/app/models/entities.py#L52-L65); refactored to `Numeric(12, 2)` to eliminate currency rounding drift. |
| **CHK-DB-02** | **Data & Schema Fault (Boundary Constraint)** | Are database-level `CheckConstraint` declarations enforced to prevent negative financial values (e.g., `total_savings >= 0`, `amount > 0`)? | **REMEDIATED**<br>Added `chk_savings_non_negative` and `chk_shares_non_negative` to block negative balance mutations. |
| **CHK-DB-03** | **Control Fault (Business Invariant)** | Does a database constraint or invariant check prevent a borrower from acting as their own guarantor (`borrower_id != guarantor_member_id`)? | **REMEDIATED**<br>Added cross-entity constraint in [`entities.py`](file:///c:/Users/user/Documents/Quality%20assurance/SWE-3020-GROUP_PROJECT/app/models/entities.py#L96) and validation guard in loan application pipeline. |
| **CHK-DB-04** | **Data & Security Fault (Idempotency)** | Is the external payment reference code (`MpesaReceiptNumber`) enforced with a unique index to block duplicate deposits / double-spending? | **PASSED**<br>Enforced `unique=True, index=True` on `LedgerTransaction.reference_code`; duplicate callback attempts rejected by DB. |
| **CHK-DB-05** | **Storage Management Fault (Referential Integrity)** | Do foreign keys on immutable financial and audit records specify `ondelete="RESTRICT"` rather than defaulting to cascading deletion? | **REMEDIATED**<br>Specified `ondelete="RESTRICT"` on `member_id` foreign keys to prevent accidental deletion of historical audit trails. |
| **CHK-DB-06** | **Control Fault (Atomicity / ACID)** | Are multi-step balance mutations and ledger insertions wrapped in a single atomic transaction block (`with db.begin_nested():`)? | **REMEDIATED**<br>Eliminated split `db.commit()` calls in [`app/services/ledger.py`](file:///c:/Users/user/Documents/Quality%20assurance/SWE-3020-GROUP_PROJECT/app/services/ledger.py); all balance and ledger writes commit atomically. |
| **CHK-DB-07** | **Exception Management Fault (Rollback Safety)** | Does every transactional write block contain an explicit `db.rollback()` within an `except Exception:` block? | **REMEDIATED**<br>Wrapped financial write services in `try/except` with guaranteed `db.rollback()` to prevent hanging SQLite write locks. |
| **CHK-DB-08** | **Control Fault (Concurrency / Locking)** | Are concurrent account modifications protected using pessimistic row-level locking (`with_for_update()`) to prevent lost updates? | **REMEDIATED**<br>Added `.with_for_update()` to serialize simultaneous M-Pesa IPN callback deposits on identical accounts. |
| **CHK-DB-09** | **Storage Management Fault (Session Leakage)** | Are SQLAlchemy sessions closed on 100% of execution paths using context managers or FastAPI's `yield get_db`? | **PASSED**<br>Verified that all API controllers inject `get_db` dependency with guaranteed `finally: db.close()`. |
| **CHK-DB-10** | **Storage & Query Fault (Performance / N+1)** | Are relational joins on account statements and loan rosters eagerly loaded (`joinedload`) to eliminate N+1 query explosion? | **REMEDIATED**<br>Added `joinedload(SavingsAccount.transactions)` in statement generator to prevent query explosion. |

---

## 4. Domain-Specific Extensions for SWE3020B (Security & Financial Integrity)

Because the **Sacco Digital Savings Tracker** manages real community assets and credit, standard syntactic checks must be augmented with Financial Invariant and Security Checks.

### Table 2: Financial Integrity & Security Invariant Checks

| Dimension | Inspection Check Question | Implementation Standard |
| :--- | :--- | :--- |
| **Financial Ledger Integrity** | • Is every balance update modeled as an immutable, append-only ledger transaction (Double-Entry)?<br>• Is direct manual mutation of `member.total_savings` forbidden outside of reconciled ledger entries?<br>• Does the system verify `Debit Total == Credit Total` before committing financial batches? | ACID Invariance, Audit Ledger Traceability (`LedgerModule`). |
| **Race Conditions & Double-Spend** | • Are concurrent loan disbursements or deposit confirmations protected with database row-level locking (`SELECT ... FOR UPDATE`) or transactional mutexes?<br>• Are M-Pesa transaction IDs (`MpesaReceiptNumber`) validated for uniqueness with a unique database index to prevent duplicate credit? | Idempotency Key Enactment (`MPESA_RECEIPT_IDX`). |
| **Authentication & RBAC (OWASP ASVS)** | • Are endpoints protected by role-verifying dependencies (`require_roles(["TREASURER", "ADMIN"])`) rather than solely relying on frontend hiding?<br>• Are JWT tokens validated for signature, expiration (`exp`), and revoked status before processing sensitive actions?<br>• Are passwords hashed using modern adaptive algorithms (Argon2id or bcrypt) with work factor $\ge 12$? | OWASP ASVS Level 2, Role-Based Access Control. |
| **Guarantor Endorsement Protocol** | • Can a borrower guarantee their own loan? (Check: `borrower_id != guarantor_id`).<br>• Does the system check whether a guarantor's free shares equal or exceed the guaranteed portion? | Chama Bylaw Invariants (`LoanEngineModule`). |

---

## 4. Real-World Inspection Walkthroughs (Codebase Case Studies)

To demonstrate the application of this checklist in the SWE3020B CAT 2 defense, the following actual examples illustrate defects detected during inspection.

### Case Study 1: Interface & Control Fault in `ProtectedRoute.jsx`
* **Defect Class:** Interface Fault (Missing Parameter) & Control Fault (Unbound Reference).
* **Inspected Code:**
  ```javascript
  // Defective Code
  export default function ProtectedRoute({ children }) {
      const user = JSON.parse(localStorage.getItem("user") || "null");
      if (!user) return <Navigate to="/login" replace={true} />;
      
      // 'role' is evaluated but was never destructured in the function signature!
      if (role && user.role !== role) return <Navigate to="/unauthorized" replace={true} />;
      return children;
  }
  ```
* **Inspection Finding:** The function signature accepts only `{ children }`. Evaluating `role` on line 5 results in an uncaught `ReferenceError: role is not defined`, crashing the React application for any protected route.
* **Remediation:**
  ```javascript
  // Corrected Code
  export default function ProtectedRoute({ children, role }) {
      const user = JSON.parse(localStorage.getItem("user") || "null");
      if (!user) return <Navigate to="/login" replace={true} />;
      if (role && user.role !== role) return <Navigate to="/unauthorized" replace={true} />;
      return children;
  }
  ```

---

### Case Study 2: Storage Management & Exception Fault in SQLAlchemy Service
* **Defect Class:** Storage Management Fault (Unclosed Session) & Exception Management Fault (Missing Rollback).
* **Inspected Code:**
  ```python
  # Defective Code
  def record_member_deposit(member_id: int, amount: float):
      db = SessionLocal()
      member = db.query(Member).filter(Member.id == member_id).first()
      member.savings_balance += amount  # Float rounding risk + direct mutation
      db.commit()
      return member
  ```
* **Inspection Finding:**
  1. If `db.commit()` raises an operational exception (e.g. database disk full or lock), no rollback is triggered.
  2. The session `db` is never closed in a `finally` block, causing connection pool starvation.
  3. Floating-point arithmetic on currency leads to IEEE 754 precision loss.
* **Remediation:**
  ```python
  # Corrected Code
  from decimal import Decimal

  def record_member_deposit(db: Session, member_id: int, amount: Decimal):
      try:
          with db.begin_nested():
              member = db.query(Member).with_for_update().filter(Member.id == member_id).first()
              if not member:
                  raise ResourceNotFoundError(f"Member {member_id} does not exist.")
              
              # Append-only immutable ledger record
              ledger_entry = LedgerTransaction(
                  member_id=member.id,
                  type=TransactionType.DEPOSIT,
                  amount=amount,
                  status=TransactionStatus.CONFIRMED
              )
              db.add(ledger_entry)
              member.savings_balance += amount
          db.commit()
          return member
      except Exception:
          db.rollback()
          raise
  ```

---

## 5. Formal Defect Logging Template (IEEE 1028 Format)

Use this tabular format during formal inspection meetings to record findings:

| Inspection ID | Date | Module / File | Line(s) | Fault Class | Severity (Crit/High/Med/Low) | Description of Defect | Assigned Reviewer | Author Fix Verified |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **INS-001** | 2026-10-26 | `frontend/.../ProtectedRoute.jsx` | 3, 5 | Interface / Control | **HIGH** | `role` prop not destructured; causes runtime `ReferenceError`. | Mercy T. | [X] Fixed & Verified |
| **INS-002** | 2026-10-27 | `app/services/loan_calculator.py` | 42 | Data Fault | **MEDIUM** | Interest rounded using default float instead of `Decimal(ROUND_HALF_UP)`. | Jescah O. | [X] Fixed & Verified |
| **INS-003** | 2026-10-28 | `app/api/v1/mpesa.py` | 78 | Exception Fault | **HIGH** | M-Pesa callback handler missing try/except on malformed JSON dictionary keys. | Tayak R. | [X] Fixed & Verified |
| **INS-004** | 2026-10-28 | `app/services/ledger.py` | 115 | Storage Fault | **HIGH** | Missing `db.rollback()` on transaction failure causing hanging SQLite write lock. | Mercy T. | [X] Fixed & Verified |

---

## 6. How to Present This in Your Project Defense

When asked by the panel or Prof. Eunice Mwangi about how your team ensured code quality:
1. **Highlight the Standard:** *"We adopted IEEE 1028-2008 formal inspection processes governed by Ian Sommerville's 6 classic fault classes (Data, Control, I/O, Interface, Storage, and Exception faults)."*
2. **Contextualize with Financial Invariants:** *"Because this is a Sacco financial platform, we extended Sommerville's checklist to explicitly inspect for currency precision (eliminating float math), double-entry ledger immutability, and database connection lifecycle management."*
3. **Show Concrete Evidence:** Reference `INS-001` (the `ProtectedRoute.jsx` prop destructuring bug caught during PR #1 review) to show that your inspections actively intercepted runtime defects before merge.
