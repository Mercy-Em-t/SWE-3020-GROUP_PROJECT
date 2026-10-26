# Jira Board Simulation & Task Implementation Register
**Project:** Sacco Digital Savings Tracker  
**Course:** SWE3020B – Software Quality Assurance and Security (USIU-Africa)  
**Deliverable:** CAT 2 Project Management & Teamwork Evaluation (30 Marks)  
**Board Type:** Jira Agile Scrum / Kanban Board  

---

## 1. Visual Jira Board Simulation (Current Sprint 2 State)

```
=======================================================================================================================================
|  1. BACKLOG (6 pts)    |  2. TO DO (5 pts)       |  3. IN PROGRESS (11 pts) |  4. CODE REVIEW (11 pts)|  5. QA TESTING (8 pts) |  6. DONE (41 pts)     |
=======================================================================================================================================
| [SACCO-124]            | [SACCO-125]             | [SACCO-110]              | [SACCO-113]             | [SACCO-120]            | [SACCO-101]           |
| Production Docker      | Slide Deck & Demo       | Bank Transfer Gateway    | Loan Amortization &     | PyTest Integration API | FastAPI Core Scaffolding|
| Containerization       | Rehearsal               | Strategy Adapter         | Late Penalties          | Journey Test           | Assignee: Mercy (5pts)|
| Assignee: Roy (3 pts)  | Assignee: Roy (5 pts)   | Assignee: Jescah (3 pts) | Assignee: Jescah (5 pts)| Assignee: Tayak (5 pts)|                       |
|                        |                         |                          |                         |                        | [SACCO-102]           |
| [SACCO-118]            |                         | [SACCO-114]              | [SACCO-117]             | [SACCO-121]            | JWT Auth & Password   |
| High-Contrast WCAG     |                         | Guarantor Coverage       | Figma Client State      | Boundary Failure &     | Hashing (PBKDF2)      |
| Dark Theme Polish      |                         | Multi-Party Logic        | Store Integration       | Limit Tests            | Assignee: Mercy (5pts)|
| Assignee: Nyeliep(3pts)|                         | Assignee: Mercy (8 pts)  | Assignee: Roy (6 pts)   | Assignee: Tayak (3 pts)|                       |
|                        |                         |                          |                         |                        | [SACCO-103]           |
|                        |                         |                          |                         |                        | Relational DB Schema  |
|                        |                         |                          |                         |                        | Models (SQLAlchemy)   |
|                        |                         |                          |                         |                        | Assignee: Mercy (5pts)|
|                        |                         |                          |                         |                        |                       |
|                        |                         |                          |                         |                        | [SACCO-107]           |
|                        |                         |                          |                         |                        | Double-Entry Atomic   |
|                        |                         |                          |                         |                        | Ledger Repository     |
|                        |                         |                          |                         |                        | Assignee: Jescah (8pts)|
|                        |                         |                          |                         |                        |                       |
|                        |                         |                          |                         |                        | [SACCO-108]           |
|                        |                         |                          |                         |                        | M-Pesa Daraja STK Push|
|                        |                         |                          |                         |                        | Strategy Adapter      |
|                        |                         |                          |                         |                        | Assignee: Jescah (5pts)|
|                        |                         |                          |                         |                        |                       |
|                        |                         |                          |                         |                        | [SACCO-111]           |
|                        |                         |                          |                         |                        | 3x Shares Borrowing   |
|                        |                         |                          |                         |                        | Limit Rule Engine     |
|                        |                         |                          |                         |                        | Assignee: Mercy (5pts)|
|                        |                         |                          |                         |                        |                       |
|                        |                         |                          |                         |                        | [SACCO-115]           |
|                        |                         |                          |                         |                        | High-Fidelity Figma UI|
|                        |                         |                          |                         |                        | Design Deliverables   |
|                        |                         |                          |                         |                        | Assignee: Nyeliep(5pts)|
|                        |                         |                          |                         |                        |                       |
|                        |                         |                          |                         |                        | [SACCO-122]           |
|                        |                         |                          |                         |                        | GitHub Actions CI/CD  |
|                        |                         |                          |                         |                        | Lint & PyTest Pipeline|
|                        |                         |                          |                         |                        | Assignee: Mercy (3pts)|
=======================================================================================================================================
```

### Sprint Metrics Summary
* **Total Committed Story Points:** 82 Story Points
* **Completed (Done):** 41 Story Points (**50%**)
* **Active Pipeline (In Progress / Review / QA):** 30 Story Points (**36.5%**)
* **Remaining Sprint Backlog (To Do / Backlog):** 11 Story Points (**13.5%**)

---

## 2. Exhaustive Task Breakdown & Implementation Notes

### EPIC 1: Architecture, Core Infrastructure & Database Engine
**Epic Goal:** Establish the layered Controller-Service-Repository architecture, environment configurations, and SQLAlchemy relational models.

---

#### Ticket ID: `SACCO-101`
* **Summary:** Scaffold FastAPI application framework and layered package hierarchy
* **Type:** Task | **Story Points:** 5 | **Priority:** High | **Status:** **DONE**
* **Assignee:** Mercy Tryphen | **Target Branch:** `feature/backend-core`
* **Implementation Notes:**
  * Scaffold directory structure (`app/core`, `app/api`, `app/models`, `app/schemas`, `app/services`, `app/repositories`, `app/gateways`, `app/interfaces`).
  * Initialize `FastAPI` instance in `app/main.py` with custom OpenAPI metadata, `/docs` Swagger UI endpoints, and CORS middleware allowing frontend origin connection.
  * Define `app/core/config.py` with default borrowing constants ($3.0\times$), interest rates ($12\%$), and grace periods ($5\text{ days}$).
* **Acceptance Criteria (Gherkin):**
  ```gherkin
  Scenario: FastAPI server initializes cleanly
    Given the environment dependencies are installed from requirements.txt
    When the uvicorn development server starts on port 8000
    Then the health check endpoint GET / returns HTTP 200 with status "online"
    And navigating to /docs renders interactive Swagger UI documentation
  ```

---

#### Ticket ID: `SACCO-102`
* **Summary:** Implement Identity Management, PBKDF2 Password Hashing, and JWT Session RBAC
* **Type:** User Story | **Story Points:** 5 | **Priority:** Critical | **Status:** **DONE**
* **Assignee:** Mercy Tryphen | **Target Branch:** `feature/backend-core`
* **Implementation Notes:**
  * Implement PBKDF2-HMAC-SHA256 password salting and verification in `app/core/security.py`.
  * Implement signed token creation (`create_access_token`) and decoding (`decode_access_token`).
  * Enforce role-based access validation distinguishing `member`, `treasurer`, and `admin`.
* **Acceptance Criteria:**
  ```gherkin
  Scenario: Duplicate email registration rejection
    Given a member already exists with email "mercy@sacco.org"
    When a registration request is submitted with the identical email
    Then the system rejects the request with HTTP 400 Bad Request
    And no plaintext password is saved to the database
  ```

---

#### Ticket ID: `SACCO-103`
* **Summary:** Design relational database schemas and SQLAlchemy entity models
* **Type:** Task | **Story Points:** 5 | **Priority:** High | **Status:** **DONE**
* **Assignee:** Mercy Tryphen | **Target Branch:** `feature/backend-core`
* **Implementation Notes:**
  * Implement `Base` declarative entity classes in `app/models/entities.py`:
    * `Member` (credentials, role, relationship to accounts and loans)
    * `SavingsAccount` (total shares, total liquid savings)
    * `LedgerTransaction` (append-only ledger row, reference code, balance progression)
    * `Loan` (principal, flat interest rate, duration, outstanding balance, status)
    * `GuarantorCommitment` (foreign keys to loan and guarantor member)
    * `AuditLog` (actor email, action, entity ID, delta, timestamp)
* **Acceptance Criteria:**
  ```gherkin
  Scenario: Database tables generate successfully on engine startup
    Given a fresh SQLite / PostgreSQL database connection
    When Base.metadata.create_all(bind=engine) executes
    Then 6 relational tables are created with proper unique constraints and foreign keys
  ```

---

### EPIC 2: Transactional Core & Double-Entry Ledger
**Epic Goal:** Deliver automated contribution tracking, payment abstraction, and append-only ledger journals.

---

#### Ticket ID: `SACCO-107`
* **Summary:** Engineer atomic, append-only double-entry ledger repository
* **Type:** User Story | **Story Points:** 8 | **Priority:** Critical | **Status:** **DONE**
* **Assignee:** Jescah Otwoma | **Target Branch:** `feature/backend-core`
* **Implementation Notes:**
  * Build `LedgerRepository` in `app/repositories/ledger_repo.py`.
  * Enforce ACID transaction boundaries: when a deposit is credited, both `SavingsAccount.total_savings` and `total_shares` increment, while an immutable `LedgerTransaction` row is appended in the same commit.
  * Disallow `UPDATE` or `DELETE` operations on historical `LedgerTransaction` rows.
* **Acceptance Criteria:**
  ```gherkin
  Scenario: Atomic deposit crediting
    Given Member 2 has an initial savings balance of KES 25,000
    When a deposit of KES 5,000 is logged with reference "MPESA_123"
    Then the new balance evaluates strictly to KES 30,000
    And a new ledger row is persisted with balance_after = 30000.0
  ```

---

#### Ticket ID: `SACCO-108`
* **Summary:** Implement Safaricom Daraja M-Pesa STK Push payment gateway adapter
* **Type:** User Story | **Story Points:** 5 | **Priority:** High | **Status:** **DONE**
* **Assignee:** Jescah Otwoma | **Target Branch:** `feature/backend-core`
* **Implementation Notes:**
  * Define `IPaymentGateway` abstract strategy interface in `app/interfaces/payment.py` (OCP/ISP).
  * Implement `MpesaDarajaGateway` in `app/gateways/mpesa_gateway.py`.
  * Return standardized `PaymentResult` model containing `transaction_reference`, `amount`, and provider response code.
* **Acceptance Criteria:**
  ```gherkin
  Scenario: Initiating mobile money contribution
    Given a valid member phone number "+254712345678" and amount KES 5,000
    When initiate_deposit() is invoked
    Then a success PaymentResult is returned with a unique reference code starting with "DAR_"
  ```

---

#### Ticket ID: `SACCO-110`
* **Summary:** Implement secondary Bank Transfer / Wire gateway strategy adapter
* **Type:** Task | **Story Points:** 3 | **Priority:** Medium | **Status:** **IN PROGRESS**
* **Assignee:** Jescah Otwoma | **Target Branch:** `feature/payment-adapters`
* **Implementation Notes:**
  * Build `BankTransferGateway` in `app/gateways/bank_gateway.py` implementing `IPaymentGateway`.
  * Demonstrates Liskov Substitution Principle (LSP): can be swapped into `SavingsLedgerService` dynamically when `payment_channel="bank"` without changing service code.
* **Acceptance Criteria:**
  ```gherkin
  Scenario: Depositing via Bank EFT channel
    Given a deposit request with payment_channel = "bank"
    When process_deposit() executes
    Then BankTransferGateway handles the transaction returning an "EFT_" reference code
  ```

---

### EPIC 3: Credit Engine, Borrowing Limits & Amortization
**Epic Goal:** Implement rule-based loan eligibility ($3\times\text{Shares}$), guarantor commitment validation, and delinquency penalties.

---

#### Ticket ID: `SACCO-111`
* **Summary:** Implement dynamic borrowing limit calculation engine ($3.0\times\text{Shares}$)
* **Type:** User Story | **Story Points:** 5 | **Priority:** Critical | **Status:** **DONE**
* **Assignee:** Mercy Tryphen | **Target Branch:** `feature/backend-core`
* **Implementation Notes:**
  * Create `LoanCalculationService` in `app/services/loan_service.py` implementing `ILoanCalculator` (SRP).
  * Formula: $\text{Limit} = \text{Total Accumulated Shares} \times 3.0$.
  * Boundary logic: Returns `0.0` if shares are zero or negative.
* **Acceptance Criteria:**
  ```gherkin
  Scenario: Member checks maximum borrowing limit
    Given a member has KES 25,000 in accumulated shares
    When calculate_borrowing_limit() is invoked
    Then the resulting limit is strictly KES 75,000.0
  ```

---

#### Ticket ID: `SACCO-113`
* **Summary:** Build amortization schedule and 5-day grace period delinquency penalty calculator
* **Type:** User Story | **Story Points:** 5 | **Priority:** High | **Status:** **IN CODE REVIEW**
* **Assignee:** Jescah Otwoma | **Target Branch:** `feature/backend-core`
* **Implementation Notes:**
  * Implement flat-rate monthly amortization: $\text{Interest} = \text{Principal} \times (\text{Rate} \times \frac{\text{Months}}{12})$.
  * Implement late fee penalty logic: If overdue days $> 5$ (grace period), assess a $5\%$ penalty on the overdue balance.
* **Acceptance Criteria:**
  ```gherkin
  Scenario: Delinquency penalty assessment boundary
    Given an overdue loan balance of KES 10,000
    When late days is 5 days (within grace period)
    Then penalty is KES 0.0
    When late days is 6 days (past grace period)
    Then penalty evaluates strictly to KES 500.0 (5% of 10,000)
  ```

---

#### Ticket ID: `SACCO-114`
* **Summary:** Implement multi-party guarantor coverage sufficiency validation
* **Type:** User Story | **Story Points:** 8 | **Priority:** Critical | **Status:** **IN PROGRESS**
* **Assignee:** Mercy Tryphen | **Target Branch:** `feature/backend-core`
* **Implementation Notes:**
  * Implement `validate_guarantor_coverage` in `app/services/loan_service.py`.
  * Calculate uncollateralized shortfall: $\text{Shortfall} = \max(0, \text{Principal} - \text{Applicant Shares})$.
  * Verify that $\sum \text{Guarantor Commitments} \ge \text{Shortfall}$. Reject with HTTP 400 if insufficient.
* **Acceptance Criteria:**
  ```gherkin
  Scenario: Loan application rejected for guarantor shortfall
    Given Member shares = KES 10,000 and requested loan = KES 25,000 (shortfall = KES 15,000)
    When a single guarantor pledges only KES 5,000
    Then the loan application is rejected with HTTP 400 "guarantor coverage shortfall"
  ```

---

### EPIC 4: UI/UX Prototyping & Figma Client Integration
**Epic Goal:** Deliver user-friendly, high-contrast, WCAG 2.1 accessible interfaces mapped to backend APIs.

---

#### Ticket ID: `SACCO-115`
* **Summary:** Deliver High-Fidelity interactive Figma prototype for core user journeys
* **Type:** Task | **Story Points:** 5 | **Priority:** High | **Status:** **DONE**
* **Assignee:** Nyeliep Nial | **Target:** Figma Deliverable
* **Implementation Notes:**
  * Build responsive layouts for: Member Dashboard, Deposit Modal, Loan Application Wizard, Ledger Journal, and Treasurer Console in Figma.
  * Apply WCAG 2.1 AA compliant color contrasts (Deep Navy `#1F4E79`, Emerald Accent, Charcoal text).
* **Acceptance Criteria:**
  ```gherkin
  Scenario: Figma prototype evaluation
    Given the public Figma prototype link
    When the evaluator clicks through the member deposit and loan application journeys
    Then all interactive modals, input forms, and confirmation states display with high contrast
  ```

---

#### Ticket ID: `SACCO-117`
* **Summary:** Create frontend state models and client fetch hooks connecting to FastAPI
* **Type:** Task | **Story Points:** 6 | **Priority:** High | **Status:** **IN CODE REVIEW**
* **Assignee:** Roy | **Target Branch:** `feature/frontend-ui`
* **Implementation Notes:**
  * Write reusable JavaScript API client `saccoApi.js` calling `http://127.0.0.1:8000/api/v1`.
  * Connect frontend state stores to backend endpoints for authentication, dashboard balances, and deposit submissions.
* **Acceptance Criteria:**
  ```gherkin
  Scenario: Client fetches live member dashboard
    Given a logged-in member with ID 2
    When the client triggers getMemberDashboard()
    Then live data from GET /api/v1/savings/account/2 populates the UI cards without CORS errors
  ```

---

#### Ticket ID: `SACCO-118`
* **Summary:** Polish UI accessibility, micro-interactions, and mobile responsiveness
* **Type:** Task | **Story Points:** 3 | **Priority:** Low | **Status:** **BACKLOG**
* **Assignee:** Nyeliep Nial | **Target:** Sprint 3 Backlog

---

### EPIC 5: Software Quality Assurance, Testing & CI/CD
**Epic Goal:** Guarantee mathematical correctness, zero regression bugs, and automated continuous verification.

---

#### Ticket ID: `SACCO-120`
* **Summary:** Build automated PyTest integration test suite covering end-to-end user journeys
* **Type:** Task | **Story Points:** 5 | **Priority:** Critical | **Status:** **QA TESTING**
* **Assignee:** Tayak Ruai | **Target Branch:** `feature/backend-core`
* **Implementation Notes:**
  * Implement `tests/integration/test_api_endpoints.py` using FastAPI `TestClient` and SQLite in-memory `StaticPool`.
  * Validate end-to-end journey: Register $\rightarrow$ Login $\rightarrow$ Deposit KES 20k $\rightarrow$ Check 3x limit (KES 60k) $\rightarrow$ Apply for KES 45k loan with guarantor $\rightarrow$ Repay KES 10k $\rightarrow$ Inspect audit logs.
* **Acceptance Criteria:**
  ```gherkin
  Scenario: Full integration test passes in CI
    When pytest tests/integration/ executes
    Then all 7 journey steps execute with HTTP status codes matching expectations
  ```

---

#### Ticket ID: `SACCO-121`
* **Summary:** Engineer boundary value analysis unit tests for credit thresholds & invariants
* **Type:** Task | **Story Points:** 3 | **Priority:** High | **Status:** **QA TESTING**
* **Assignee:** Tayak Ruai | **Target Branch:** `feature/backend-core`
* **Implementation Notes:**
  * Implement `tests/unit/test_loan_calculator.py` and `tests/unit/test_loan_api_validation.py`.
  * Cover negative values, zero shares, delinquency boundaries (day 5 vs day 6), and guarantor shortfalls.
* **Acceptance Criteria:**
  ```gherkin
  Scenario: 100% boundary test passing rate
    When pytest tests/unit/ executes
    Then all 15 unit test scenarios pass in under 0.3 seconds
  ```

---

#### Ticket ID: `SACCO-122`
* **Summary:** Automate GitHub Actions CI/CD workflow running Flake8 and PyTest on every push/PR
* **Type:** Task | **Story Points:** 3 | **Priority:** High | **Status:** **DONE**
* **Assignee:** Mercy Tryphen | **Target:** `.github/workflows/backend-ci.yml`
* **Implementation Notes:**
  * Configure workflow on push/PR for `main`, `develop`, and `feature/*`.
  * Step 1: Python 3.11 setup + dependency installation.
  * Step 2: `flake8 app tests` enforcing PEP-8 compliance (0 errors).
  * Step 3: `pytest -v` executing full test suite.
* **Acceptance Criteria:**
  ```gherkin
  Scenario: Automated pull request verification
    Given an open pull request to develop or main
    When commits are pushed to the branch
    Then GitHub Actions pipeline runs and displays a green checkmark
  ```

---

#### Ticket ID: `SACCO-124`
* **Summary:** Multi-stage production Docker containerization and Docker Compose orchestration
* **Type:** Task | **Story Points:** 3 | **Priority:** Medium | **Status:** **BACKLOG**
* **Assignee:** Roy | **Target:** `Dockerfile`, `docker-compose.yml`

---

### EPIC 6: Evaluation Presentation & Live Walkthrough
**Epic Goal:** Synchronize speaking roles, slide deck visuals, and live execution run-sheet for Wednesday.

---

#### Ticket ID: `SACCO-125`
* **Summary:** Compile final 12-slide presentation deck and live Swagger UI walkthrough script
* **Type:** Task | **Story Points:** 5 | **Priority:** Critical | **Status:** **TO DO**
* **Assignee:** Roy | **Target:** Slide Deck & Script
* **Implementation Notes:**
  * Format 12-slide presentation deck matching Prof. Eunice Mwangi's 30-mark rubric.
  * Pre-seed database accounts using `app/seed.py` for live demo walkthrough (Member Mercy, Guarantor Jescah, Admin Eunice).
  * Run mock presentation rehearsal with all 5 members.
* **Acceptance Criteria:**
  ```gherkin
  Scenario: Presentation timing rehearsal
    Given all 5 members present their assigned slides
    When the live demo on http://127.0.0.1:8000/docs executes
    Then the entire walkthrough completes within the allocated 10-minute window
  ```
