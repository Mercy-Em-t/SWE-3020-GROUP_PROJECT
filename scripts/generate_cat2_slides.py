import os
import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def create_presentation():
    prs = pptx.Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Color Palette - Emerald Green & Executive Slate Theme
    NAVY = RGBColor(15, 32, 39)
    DARK_BG = RGBColor(20, 30, 45)
    EMERALD = RGBColor(16, 185, 129)
    CYAN = RGBColor(6, 182, 212)
    WHITE = RGBColor(255, 255, 255)
    LIGHT_BG = RGBColor(248, 250, 252)
    CARD_BG = RGBColor(255, 255, 255)
    BORDER_COLOR = RGBColor(226, 232, 240)
    TEXT_MAIN = RGBColor(30, 41, 59)
    TEXT_MUTED = RGBColor(100, 116, 139)
    GREEN_ACCENT = RGBColor(5, 150, 105)

    def add_header(slide, title_text, category_badge, subtitle_text):
        # Header background banner
        header_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.733), Inches(1.1))
        tf = header_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p_badge = tf.paragraphs[0]
        p_badge.text = category_badge.upper()
        p_badge.font.size = Pt(11)
        p_badge.font.bold = True
        p_badge.font.color.rgb = EMERALD

        p_title = tf.add_paragraph()
        p_title.text = title_text
        p_title.font.size = Pt(24)
        p_title.font.bold = True
        p_title.font.color.rgb = TEXT_MAIN

        if subtitle_text:
            p_sub = tf.add_paragraph()
            p_sub.text = subtitle_text
            p_sub.font.size = Pt(13)
            p_sub.font.color.rgb = TEXT_MUTED

    def add_card(slide, left, top, width, height, title, items, badge=""):
        # Card container shape
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
        shape.fill.solid()
        shape.fill.fore_color.rgb = CARD_BG
        shape.line.color.rgb = BORDER_COLOR
        shape.line.width = Pt(1.5)

        tb = slide.shapes.add_textbox(Inches(left + 0.3), Inches(top + 0.25), Inches(width - 0.6), Inches(height - 0.5))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        if badge:
            p_b = tf.paragraphs[0]
            p_b.text = badge.upper()
            p_b.font.size = Pt(10)
            p_b.font.bold = True
            p_b.font.color.rgb = GREEN_ACCENT
            p_t = tf.add_paragraph()
        else:
            p_t = tf.paragraphs[0]

        p_t.text = title
        p_t.font.size = Pt(17)
        p_t.font.bold = True
        p_t.font.color.rgb = TEXT_MAIN
        p_t.space_after = Pt(10)

        for item in items:
            p = tf.add_paragraph()
            p.text = "• " + item
            p.font.size = Pt(12)
            p.font.color.rgb = TEXT_MAIN
            p.space_after = Pt(6)

    # -------------------------------------------------------------
    # SLIDE 1: Title Slide (Dark Executive Theme)
    # -------------------------------------------------------------
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = NAVY
    bg1.line.fill.background()

    tb1 = s1.shapes.add_textbox(Inches(1.0), Inches(1.2), Inches(11.333), Inches(2.2))
    tf1 = tb1.text_frame
    tf1.word_wrap = True

    p0 = tf1.paragraphs[0]
    p0.text = "SWE3020B – SOFTWARE QUALITY ASSURANCE & SECURITY | CAT 2 DEFENSE (30 MARKS)"
    p0.font.size = Pt(12)
    p0.font.bold = True
    p0.font.color.rgb = EMERALD

    p1 = tf1.add_paragraph()
    p1.text = "Sacco Digital Savings Tracker"
    p1.font.size = Pt(36)
    p1.font.bold = True
    p1.font.color.rgb = WHITE
    p1.space_before = Pt(8)

    p2 = tf1.add_paragraph()
    p2.text = "Architectural Derivation, SOLID Principles, Automated SQA & CI/CD Verification"
    p2.font.size = Pt(16)
    p2.font.color.rgb = CYAN
    p2.space_before = Pt(6)

    # Team Roster Card on Slide 1
    team_box = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(3.8), Inches(11.333), Inches(2.8))
    team_box.fill.solid()
    team_box.fill.fore_color.rgb = RGBColor(26, 44, 60)
    team_box.line.color.rgb = RGBColor(40, 65, 88)

    t_tb = s1.shapes.add_textbox(Inches(1.3), Inches(4.0), Inches(10.733), Inches(2.4))
    t_tf = t_tb.text_frame
    t_tf.word_wrap = True

    tp0 = t_tf.paragraphs[0]
    tp0.text = "EVALUATION ROSTER & APPORTIONED ROLES (Prof. Eunice Mwangi):"
    tp0.font.size = Pt(12)
    tp0.font.bold = True
    tp0.font.color.rgb = EMERALD
    tp0.space_after = Pt(10)

    members = [
        "Mercy Tryphen (Lead) – System Architecture & Backend Infrastructure (ID: 674748)",
        "Jescah Otwoma – API Contracts & Payment Gateways (ID: 673748)",
        "Nyeliep Nial – Frontend UI/UX Design & Client Architecture (ID: 673176)",
        "Tayak Ruai – SQA & Automated Test Engineering (ID: 671649)",
        "Roy Githaiga – Client Integration & Agile Scrum Facilitator"
    ]
    for m in members:
        p = t_tf.add_paragraph()
        p.text = "• " + m
        p.font.size = Pt(13)
        p.font.color.rgb = WHITE
        p.space_after = Pt(4)

    s1.notes_slide.notes_text_frame.text = (
        "Presenter: Mercy (Lead)\n"
        "Talking Point: Good morning Professor Eunice. Today our team presents the Sacco Digital Savings Tracker. "
        "Our project is structured across five dedicated engineering roles to satisfy the full 30-mark CAT 2 rubric, "
        "covering Software Design Principles, SOLID implementation, automated testing pyramid, and CI/CD pipelines."
    )

    # -------------------------------------------------------------
    # SLIDE 2: Project Context & Problem Breakdown [2 Marks]
    # -------------------------------------------------------------
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "Project Context & Problem Domain Analysis", "Rubric Deliverable: Project Context & Use Cases (2 Marks)",
               "Deconstructing manual spreadsheet SACCO failures into automated mathematical invariants.")

    add_card(s2, 0.8, 1.8, 5.7, 5.0, "The 3 Real-World Failure Modes of Manual SACCOs", [
        "Trust Deficit (Information Asymmetry): Members cannot independently audit physical cash banked vs manual passbooks.",
        "Phantom Borrowing Limits: Treasurers calculate borrowing capacity on paper, issuing uncollateralized loans exceeding group reserves.",
        "Guarantor Default Cascades: When a borrower defaults, informal paper pledges lack legally binding, immutable share-attachment records.",
        "Manual Bookkeeping Errors: Excel spreadsheets lack double-entry validation, causing silent balance leakage."
    ], "Problem Analysis")

    add_card(s2, 6.8, 1.8, 5.7, 5.0, "Our Engineering Solution & Domain Invariants", [
        "Automated Double-Entry Ledger: Every transaction writes debit and credit journals where Debit - Credit = 0.",
        "Deterministic Borrowing Limit: Strictly enforces Loan <= 3 * Shares directly in the domain core.",
        "Guarantor Collateral Lock: Rejects loans unless 2 active guarantors pledge sufficient shares to back the unsecured risk.",
        "Role-Based Dual Portals: Strict separation of privileges (Member personal savings vs. Admin/Treasurer group oversight)."
    ], "Architectural Solution")

    s2.notes_slide.notes_text_frame.text = (
        "Presenter: Roy / Mercy\n"
        "Talking Point: Manual SACCOs and chamas in Kenya fail for three core reasons: lack of visibility, manual borrowing calculations "
        "that lead to phantom loans, and unenforced guarantor pledges. We engineered this system from the ground up to replace human trust "
        "with immutable cryptographic ledgers and mathematical invariants."
    )

    # -------------------------------------------------------------
    # SLIDE 3: Kruchten 4+1 Architectural Views [6 Marks]
    # -------------------------------------------------------------
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "System Architecture: 3-Tier Layered Decomposition", "Rubric Deliverable: Software Design Principles (6 Marks)",
               "Conforming to Kruchten 4+1 Architectural Views and David Parnas Information Hiding.")

    add_card(s3, 0.8, 1.8, 3.7, 5.0, "Presentation Tier\n(React 19 + Vite)", [
        "Component-driven UI with AppShell, StatCards, and Steppers.",
        "Client-side defensive validation and reactive charts.",
        "Isolated dual-portal routing via ProtectedRoute (Member vs Admin).",
        "Vite dev server with automatic /api proxy to FastAPI."
    ], "Tier 1: Client")

    add_card(s3, 4.8, 1.8, 3.7, 5.0, "API & Security Tier\n(FastAPI + Pydantic)", [
        "Network perimeter boundary validation via Pydantic V2 schemas.",
        "JWT Bearer authentication with role claims (RBAC).",
        "Dependency injection wiring repositories into controllers.",
        "Automated OpenAPI / Swagger interactive documentation."
    ], "Tier 2: Perimeter")

    add_card(s3, 8.8, 1.8, 3.7, 5.0, "Core Domain & Persistence\n(SQLAlchemy + DB)", [
        "Pure business services (LoanCalculator, Amortization, Penalties).",
        "Generic BaseRepository[T] abstracting SQL persistence.",
        "Relational 3NF SQLite / PostgreSQL with foreign key constraints.",
        "Append-only double-entry ledger & immutable audit log."
    ], "Tier 3: Domain Core")

    s3.notes_slide.notes_text_frame.text = (
        "Presenter: Mercy (Lead Architect)\n"
        "Talking Point: We eliminated the 'Smart UI / Fat Controller' anti-pattern. Our architecture adheres strictly to Kruchten's 4+1 views. "
        "The React frontend never makes SQL calls; it communicates with FastAPI boundary schemas that defensively reject malformed requests. "
        "The domain logic is completely isolated from the database and HTTP transport."
    )

    # -------------------------------------------------------------
    # SLIDE 4: Software Design Principles: Modularity, Reusability & Maintainability [6 Marks]
    # -------------------------------------------------------------
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "Software Design Principles: Modularity, Reusability, Maintainability", "Rubric Deliverable: Software Design Principles (6 Marks)",
               "Promoting structural separation of concerns and high cohesion across packages.")

    add_card(s4, 0.8, 1.8, 3.7, 5.0, "Modularity\n(Separation of Concerns)", [
        "Layered Tiering: app/api (HTTP) -> app/services (Business Logic) -> app/repositories (Persistence).",
        "High Cohesion: Each module has one self-contained domain responsibility.",
        "Low Coupling: Controllers never talk directly to SQLAlchemy; services never touch raw SQL.",
        "Zero Circular Dependencies: Clean acyclic package dependency graph."
    ], "Modularity")

    add_card(s4, 4.8, 1.8, 3.7, 5.0, "Reusability\n(Generic Abstractions)", [
        "Generic Repository BaseRepository[T]: Implements standard CRUD operations (get, create, list, filter) reused across Member, Loan, and Ledger entities.",
        "Cross-Cutting JWT Guards: Reusable get_current_user and get_current_admin dependencies.",
        "Defensive Schemas: Reusable phone number regex and monetary validator types."
    ], "Reusability")

    add_card(s4, 8.8, 1.8, 3.7, 5.0, "Maintainability\n(Information Hiding)", [
        "Parnas Information Hiding: Internal database schema changes do not break business logic or frontend APIs.",
        "Pure Mathematical Engines: LoanCalculatorService can be tested in 0.01s with zero database or network dependencies.",
        "Environment Parity: app/core/config.py provides zero-config safe defaults for seamless dev/prod switching."
    ], "Maintainability")

    s4.notes_slide.notes_text_frame.text = (
        "Presenter: Jescah / Mercy\n"
        "Talking Point: For the 6 marks on Software Design Principles, we demonstrate Modularity via our 3-tier Controller-Service-Repository "
        "pattern. We demonstrate Reusability through our generic BaseRepository of T, which standardizes database access without repeating code. "
        "And Maintainability through Parnas Information Hiding, meaning financial math can change without breaking database tables."
    )

    # -------------------------------------------------------------
    # SLIDE 5: SOLID Principles: Part 1 - SRP & OCP [5 Marks]
    # -------------------------------------------------------------
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "SOLID Principles: SRP & Open/Closed Principle", "Rubric Deliverable: SOLID Principles (5 Marks) - Part 1",
               "Writing scalable, maintainable, and mathematically robust financial code.")

    add_card(s5, 0.8, 1.8, 5.7, 5.0, "Single Responsibility Principle (SRP)", [
        "Violation Avoided: Controllers doing DB queries or services formatting HTTP responses.",
        "Code Implementation:",
        "• LoanCalculationService (app/services/loan_service.py): Single reason to change = amendment to SACCO bylaws or loan interest rates.",
        "• LedgerRepository (app/repositories/ledger_repo.py): Single reason to change = persistence schema alterations.",
        "• Security Module (app/core/security.py): Single responsibility = Bcrypt hashing and JWT encoding/decoding."
    ], "SRP Proof")

    add_card(s5, 6.8, 1.8, 5.7, 5.0, "Open/Closed Principle (OCP)", [
        "Core Concept: Software entities should be open for extension, but closed for modification.",
        "Code Implementation: Pluggable Payment Gateway Strategy",
        "• IPaymentGateway (app/interfaces/payment.py) defines standard contract: initiate_deposit() and verify_transaction().",
        "• MpesaDarajaGateway implements Safaricom STK Push.",
        "• BankTransferGateway implements EFT/RTGS bank rails.",
        "• Extension: Adding Airtel Money or Pesalink requires zero modifications to SavingsService!"
    ], "OCP Proof")

    s5.notes_slide.notes_text_frame.text = (
        "Presenter: Jescah (Payment Gateways)\n"
        "Talking Point: To prove SOLID principles: Under SRP, our LoanCalculationService has only one reason to change: changes in lending math. "
        "It does not know what a database or HTTP request is. Under OCP, we implemented the Strategy Pattern for payment gateways. If our SACCO "
        "adds Airtel Money tomorrow, we simply create a new class implementing IPaymentGateway without changing a single line of our savings engine."
    )

    # -------------------------------------------------------------
    # SLIDE 6: SOLID Principles: Part 2 - LSP, ISP & DIP [5 Marks]
    # -------------------------------------------------------------
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "SOLID Principles: LSP, ISP & Dependency Inversion", "Rubric Deliverable: SOLID Principles (5 Marks) - Part 2",
               "Enforcing behavioral subtyping, lean interfaces, and dependency inversion.")

    add_card(s6, 0.8, 1.8, 3.7, 5.0, "Liskov Substitution (LSP)", [
        "Subtypes must be substitutable for base types without altering correctness.",
        "Code Proof:",
        "Both MpesaDarajaGateway and BankTransferGateway implement IPaymentGateway.",
        "Any service expecting IPaymentGateway can execute transactions without checking 'if isinstance(Mpesa)' or encountering unexpected exceptions."
    ], "LSP Proof")

    add_card(s6, 4.8, 1.8, 3.7, 5.0, "Interface Segregation (ISP)", [
        "Clients should never be forced to depend on methods they do not use.",
        "Code Proof:",
        "Instead of one bloated 'ISaccoSystem' interface, we created discrete, cohesive contracts:",
        "• ILoanCalculator (pure calculations)",
        "• IPaymentGateway (payment rails)",
        "• IBaseRepository (CRUD operations)",
        "Zero fat interfaces or dummy stub methods."
    ], "ISP Proof")

    add_card(s6, 8.8, 1.8, 3.7, 5.0, "Dependency Inversion (DIP)", [
        "High-level modules must depend on abstractions, not concrete details.",
        "Code Proof:",
        "FastAPI Dependency Injection (Depends):",
        "SavingsService depends on IRepository and IPaymentGateway interfaces.",
        "In production, FastAPI injects live SQLite/Postgres; in tests, it injects MockGateways seamlessly."
    ], "DIP Proof")

    s6.notes_slide.notes_text_frame.text = (
        "Presenter: Jescah / Mercy\n"
        "Talking Point: Under LSP, our payment gateways substitute seamlessly. Under ISP, we broke down system interfaces into focused, "
        "lean contracts like ILoanCalculator and IPaymentGateway. Under DIP, high-level services depend strictly on abstractions injected via "
        "FastAPI's dependency injection container, which allows us to swap databases or mock gateways in automated tests instantly."
    )

    # -------------------------------------------------------------
    # SLIDE 7: Testing Strategy & Testing Pyramid [3 Marks]
    # -------------------------------------------------------------
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "Comprehensive Testing Strategy: The Testing Pyramid", "Rubric Deliverable: Testing (3 Marks)",
               "Automated multi-tier verification conforming to ISO/IEC/IEEE 29119.")

    add_card(s7, 0.8, 1.8, 5.7, 5.0, "The 3-Tier Testing Pyramid Hierarchy", [
        "1. Unit Testing (PyTest & Vitest):",
        "• test_loan_calculator.py (8 tests): 3x shares multiplier, zero/negative limits, reducing amortization schedules, guarantor shortfall math, 5-day grace period, 5% late penalties.",
        "• test_auth_service.py (2 tests): Bcrypt hashing and duplicate email rejection.",
        "• Vitest Client Tests (16 tests): loan.test.js, format.test.js, ProtectedRoute.test.jsx.",
        "2. Integration Testing (FastAPI TestClient):",
        "• test_api_endpoints.py: Multi-service user journey across Auth -> Savings -> Loan -> Repay with live SQLite session.",
        "3. Invariant Verification & Smoke Testing:",
        "• test_ledger_invariants.py: Verifies double-entry ledger debit - credit = 0.",
        "• pages.smoke.test.jsx: Automatically mounts all 9 screens."
    ], "Testing Hierarchy")

    add_card(s7, 6.8, 1.8, 5.7, 5.0, "Automated Test Metrics & Verification", [
        "Test Execution Speed & Reliability:",
        "• 16 Backend PyTests executed in 0.75 seconds (100% Pass Rate).",
        "• 28 Frontend Vitest tests executed in 2.23 seconds (100% Pass Rate).",
        "Defensive Security & Boundary Coverage:",
        "• Negative Deposits: System rejects deposits <= 0 with HTTP 422.",
        "• Limit Exceeded: System rejects loans > 3x shares with HTTP 422.",
        "• Insufficient Guarantors: System rejects applications with < 2 guarantors.",
        "Continuous Execution: Every commit automatically triggers PyTest in GitHub Actions CI."
    ], "Test Execution Metrics")

    s7.notes_slide.notes_text_frame.text = (
        "Presenter: Tayak Ruai (SQA & Test Engineer)\n"
        "Talking Point: For the 3 marks on Testing: We implemented the classical ISO 29119 Testing Pyramid. We have 16 backend PyTests "
        "and 28 frontend Vitest tests. Our tests cover unit math, integration across database tiers, and most importantly, double-entry ledger "
        "invariants to ensure that debits equal credits and money can never vanish. All tests run and pass in under 1 second."
    )

    # -------------------------------------------------------------
    # SLIDE 8: Agile, Version Control, CI/CD & DevOps [3 Marks]
    # -------------------------------------------------------------
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "DevOps, Version Control & CI/CD Pipelines", "Rubric Deliverable: Agile, Version Control, CI/CD & DevOps (3 Marks)",
               "Automated GitHub Actions pipelines, Gitflow branch management, and Docker containerization.")

    add_card(s8, 0.8, 1.8, 5.7, 5.0, "Version Control & Gitflow Collaboration", [
        "Branching Strategy: Protected main (release) and develop (integration), with feature/backend-core and feature/frontend branches.",
        "Collaborative PR Workflow: Formal Pull Requests (PR #1, PR #2, PR #4, PR #5) with peer code reviews and approved merges.",
        "Conflict Resolution Mastery: Resolved complex Modify/Delete git conflicts from command line, preserving team deliverables.",
        "Peer Review Register: Documented in docs/PEER_CODE_REVIEW_REGISTER.md."
    ], "Version Control")

    add_card(s8, 6.8, 1.8, 5.7, 5.0, "Automated CI/CD & DevOps Infrastructure", [
        "GitHub Actions CI Pipeline (.github/workflows/backend-ci.yml):",
        "• Step 1: actions/checkout@v4",
        "• Step 2: actions/setup-python@v5 with pip caching",
        "• Step 3: Automated dependency installation (requirements.txt)",
        "• Step 4: flake8 PEP-8 static analysis & lint enforcement",
        "• Step 5: pytest automated test execution with coverage",
        "Smart Path Filtering: Triggers backend CI only when backend files change, preventing pipeline failures on frontend-only commits.",
        "Containerization: Multi-stage Dockerfile and docker-compose.yml for environment parity across machines.",
        "Pipeline Status: GREEN PASSING on GitHub Actions (Run #40645768982)."
    ], "CI/CD & DevOps")

    s8.notes_slide.notes_text_frame.text = (
        "Presenter: Tayak / Roy\n"
        "Talking Point: For the 3 marks on Agile, Version Control, CI/CD, and DevOps: We enforce Gitflow with protected branches and peer PR reviews. "
        "Our GitHub Actions workflow automatically checks out code, sets up Python 3.11 with pip caching, lints with flake8, and executes all 16 PyTests. "
        "Our latest CI run is 100% green on GitHub. We also provide Docker Compose to ensure dev-prod environment parity."
    )

    # -------------------------------------------------------------
    # SLIDE 9: Agile Project Management & Jira Backlog [4 Marks]
    # -------------------------------------------------------------
    s9 = prs.slides.add_slide(blank_layout)
    add_header(s9, "Agile Project Management: Jira Simulation & Teamwork", "Rubric Deliverable: Teamwork & Project Management (4 Marks)",
               "Apportioned engineering responsibilities, sprint pacing, and Gherkin acceptance criteria.")

    add_card(s9, 0.8, 1.8, 5.7, 5.0, "Jira Backlog Decomposition & Epics", [
        "6 Epics Covering Full SDLC (docs/JIRA_SIMULATION_AND_TASK_REGISTER.md):",
        "• EPIC 1: System Scaffolding & Gitflow (SACCO-101 to 103)",
        "• EPIC 2: Boundary Schema & Validation Gates (SACCO-104)",
        "• EPIC 3: Domain Entity & Ledger Invariant Modeling (SACCO-105)",
        "• EPIC 4: Business Logic Isolation & SOLID Strategy (SACCO-106, 107)",
        "• EPIC 5: API Composition, RBAC & CI/CD (SACCO-108, 109)",
        "• EPIC 6: Live Evaluation Presentation & Demo Polish (SACCO-110, 111)"
    ], "Jira Epics")

    add_card(s9, 6.8, 1.8, 5.7, 5.0, "Sprint Pacing & BDD Acceptance Criteria", [
        "Two-Sprint Agile Execution:",
        "• Sprint 1 (Oct 21–25): Scaffolding, 3NF schema, boundary models.",
        "• Sprint 2 (Oct 26–28): M-Pesa STK push, loan vetting, client integration, CI/CD fix.",
        "Gherkin BDD Acceptance Criteria on Every Story:",
        "  Given a member has KES 10,000 in shares",
        "  When they apply for a loan of KES 25,000 with 2 guarantors",
        "  Then the system accepts application with HTTP 201",
        "  And status is set to PENDING for treasurer vetting",
        "Team Velocity: 17 user stories completed with clear member assignments."
    ], "Sprint Pacing & BDD")

    s9.notes_slide.notes_text_frame.text = (
        "Presenter: Roy Githaiga (Scrum Facilitator)\n"
        "Talking Point: For the 4 marks on Teamwork and Agile Project Management: We organized our work across 6 Epics and 17 User Stories in Jira. "
        "Every single story includes formal Gherkin Acceptance Criteria (Given/When/Then) so that our SQA verification was mathematically falsifiable. "
        "We operated in two focused one-week sprints, tracking velocity from initial scaffolding to final integration."
    )

    # -------------------------------------------------------------
    # SLIDE 10: Live Functional Demo Walkthrough [5 Marks]
    # -------------------------------------------------------------
    s10 = prs.slides.add_slide(blank_layout)
    add_header(s10, "Live Functional Demonstration Architecture", "Rubric Deliverable: Live System Demonstration (5 Marks)",
               "Live end-to-end walkthrough of the React Frontend and FastAPI Backend.")

    add_card(s10, 0.8, 1.8, 5.7, 5.0, "Walkthrough Sequence (What You Will See)", [
        "1. Member Authentication & RBAC Guard:",
        "• Mercy logs into Member Portal (+254712345678 / MemberPass123!).",
        "• View personal savings balance and borrowing limit (3x shares).",
        "2. M-Pesa Mobile Deposit & Ledger Posting:",
        "• Mercy deposits KES 5,000 via M-Pesa STK Push.",
        "• Double-entry journal generates immutable reference (DAR_XXXXXX).",
        "3. Loan Application Wizard with Guarantor Collateral:",
        "• Mercy applies for KES 25,000 loan with 2 active guarantors.",
        "• Boundary gate verifies borrowing limit and guarantor sufficiency."
    ], "Step 1: Member Journey")

    add_card(s10, 6.8, 1.8, 5.7, 5.0, "Admin Oversight & Audit Verification", [
        "4. Treasurer / Admin Approval Workflow:",
        "• Prof. Eunice logs into Admin Portal (+254700111222 / AdminSecure123!).",
        "• Reviews group-wide liquidity, cash reconciliation, and loan queue.",
        "• Vets and approves Mercy's pending loan with approval notes.",
        "5. Backend Swagger API & Ledger Audit Trail:",
        "• Switch to Interactive Docs (http://127.0.0.1:8000/docs).",
        "• Inspect /api/v1/savings/ledger/{id} proving balanced debit/credit.",
        "• Inspect /api/v1/audit/logs proving actor, action, and timestamp logging."
    ], "Step 2: Admin & Audit")

    s10.notes_slide.notes_text_frame.text = (
        "Presenter: All Members (Mercy -> Nyeliep -> Jescah -> Tayak -> Roy)\n"
        "Talking Point: We now transition to our live demonstration. We will show the Member Portal where Mercy deposits KES 5,000 and applies for a loan, "
        "then switch to the Admin Portal where the treasurer vets the loan, and finally inspect the Swagger API to prove double-entry ledger immutability."
    )

    output_path = os.path.join(os.getcwd(), "SWE-3020-GROUP_PROJECT", "docs", "CAT2_PRESENTATION_SACCO_TRACKER.pptx")
    prs.save(output_path)
    print(f"Presentation successfully created at: {output_path}")

if __name__ == "__main__":
    create_presentation()
