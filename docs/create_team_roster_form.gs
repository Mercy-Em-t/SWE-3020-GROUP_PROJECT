/**
 * SWE3020B - Sacco Digital Savings Tracker
 * Team Role Allocation & Contribution Audit Survey Generator
 * 
 * INSTRUCTIONS TO RUN:
 * 1. Open your browser and go to: https://script.google.com/
 * 2. Click "New project".
 * 3. Delete any existing code, paste this entire script, and click "Save" (disk icon).
 * 4. Click "Run" at the top. (Grant Google permissions if prompted).
 * 5. Check the "Execution log" at the bottom for the generated Form URL and Edit link!
 */

function createTeamRoleAssignmentForm() {
  var formTitle = "SWE3020B Team Role Allocation & Contribution Audit";
  var form = FormApp.create(formTitle);

  form.setDescription(
    "Course: SWE3020B – Software Quality Assurance and Security\n" +
    "Project: Sacco Digital Savings Tracker (CAT 2 Evaluation - 30 Marks)\n" +
    "Lecturer: Prof. Eunice Mwangi\n\n" +
    "PURPOSE:\n" +
    "This form formally audits and establishes each team member's official role, " +
    "technical deliverables completed, and designated speaking segment for the Wednesday evaluation presentation. " +
    "Your responses will be compiled directly into the Project Documentation and Slide Deck."
  );

  form.setCollectEmail(true);
  form.setAllowResponseEdits(true);

  // ==========================================
  // SECTION 1: MEMBER IDENTITY
  // ==========================================
  var sec1 = form.addSectionHeaderItem();
  sec1.setTitle("Section 1: Member Identity & Official Details");

  // Name Selection
  var nameItem = form.addListItem();
  nameItem.setTitle("Select Your Full Name")
          .setHelpText("Select your name from the official group roster.")
          .setChoiceValues([
            "Mercy Tryphen (674748)",
            "Jescah Otwoma (673748)",
            "Nyeliep Nial (673176)",
            "Ruai Tayak Gatwiech (671649)",
            "Roy",
            "Other / New Member"
          ])
          .setRequired(true);

  // Student ID confirmation
  var studentIdItem = form.addTextItem();
  studentIdItem.setTitle("Student ID Number")
               .setHelpText("Enter your 6-digit USIU-Africa Student ID.")
               .setRequired(true);

  // WhatsApp / Contact Number
  var phoneItem = form.addTextItem();
  phoneItem.setTitle("Phone / WhatsApp Number")
           .setHelpText("Used for developer group notification and Jira tagging.")
           .setRequired(true);

  // ==========================================
  // SECTION 2: OFFICIAL ROLE ASSIGNMENT
  // ==========================================
  form.addPageBreakItem().setTitle("Section 2: Primary Role & Technical Domain");

  var roleItem = form.addMultipleChoiceItem();
  roleItem.setTitle("What is your Primary Official Role on the project?")
          .setHelpText("Select the primary capacity in which you are contributing to the CAT 2 deliverables.")
          .setChoices([
            roleItem.createChoice("Lead System Architect & Backend Infrastructure Engineer"),
            roleItem.createChoice("Backend REST API Developer & Payment Gateway Specialist"),
            roleItem.createChoice("UI/UX Designer & Frontend Component Lead (Figma / Web)"),
            roleItem.createChoice("Software Quality Assurance (SQA) & Test Automation Lead"),
            roleItem.createChoice("Client State Manager, Scrum Master & Presentation Facilitator")
          ])
          .showOtherOption(true)
          .setRequired(true);

  // ==========================================
  // SECTION 3: DELIVERABLE CONTRIBUTIONS (WHAT YOU WORKED ON)
  // ==========================================
  form.addPageBreakItem().setTitle("Section 3: Technical Tasks & Artifact Contributions");

  var tasksItem = form.addCheckboxItem();
  tasksItem.setTitle("Which specific deliverables have you completed or actively contributed to?")
           .setHelpText("Select all that apply. These will be attributed to you in the official rubric submission.")
           .setChoices([
             tasksItem.createChoice("Requirements Engineering & Use Case Modeling (FR-01 to FR-10, Use Case Diagram)"),
             tasksItem.createChoice("Figma High-Fidelity UI/UX Prototyping (Dashboard, Savings, Loans, WCAG 2.1 Accessibility)"),
             tasksItem.createChoice("FastAPI Backend Architecture & Relational Schema Modeling (SQLAlchemy / SQLite)"),
             tasksItem.createChoice("Core Financial Business Logic (3x Shares Multiplier, Amortization, Delinquency Penalties)"),
             tasksItem.createChoice("Payment Integration Strategy (M-Pesa Daraja STK Push & Bank Wire Abstraction)"),
             tasksItem.createChoice("Automated PyTest Testing Suite (Unit math tests, invariant checks, API integration tests)"),
             tasksItem.createChoice("DevOps & CI/CD Automation (GitHub Actions .github/workflows, Flake8 linting, Branching strategy)"),
             tasksItem.createChoice("Jira Agile Project Management (Sprint backlog, User stories, Burndown tracking, Standups)"),
             tasksItem.createChoice("Presentation Deck Compilation (12-Slide deck formatting, speaker notes, live demo scripting)")
           ])
           .showOtherOption(true)
           .setRequired(true);

  // Key Technical Accomplishment Narrative
  var narrativeItem = form.addParagraphTextItem();
  narrativeItem.setTitle("Briefly describe the specific technical challenges you solved or are working on:")
               .setHelpText("e.g. 'I implemented the borrowing limit rule ensuring members cannot borrow more than 3x their shares', or 'I designed the Figma loan application flow'.")
               .setRequired(true);

  // ==========================================
  // SECTION 4: WEDNESDAY EVALUATION SPEAKING SEGMENT
  // ==========================================
  form.addPageBreakItem().setTitle("Section 4: Wednesday Live Presentation & Defense Allocation");

  var presentationItem = form.addMultipleChoiceItem();
  presentationItem.setTitle("Which segment of the presentation will you lead during Wednesday's evaluation?")
                  .setHelpText("Prof. Eunice Mwangi requires every member to demonstrate clear individual contribution.")
                  .setChoices([
                    presentationItem.createChoice("Segment 1: Project Overview, Context, Problem Statement & Use Case Diagram (Slides 1-5)"),
                    presentationItem.createChoice("Segment 2: UI/UX Figma Design, Usability & Accessibility Principles (Slide 6)"),
                    presentationItem.createChoice("Segment 3: Software Design Principles & SOLID Compliance (Slides 7-8)"),
                    presentationItem.createChoice("Segment 4: SQA Testing Pyramid, PyTest Suite & Code Quality (Slide 9)"),
                    presentationItem.createChoice("Segment 5: DevOps, Version Control (Git) & GitHub Actions CI/CD Pipeline (Slide 10)"),
                    presentationItem.createChoice("Segment 6: Teamwork Collaboration & Jira Agile Project Management (Slide 11)"),
                    presentationItem.createChoice("Segment 7: Live System Demonstration & Swagger UI Walkthrough (Slide 12)")
                  ])
                  .showOtherOption(true)
                  .setRequired(true);

  // Readiness / Confidence Scale
  var scaleItem = form.addScaleItem();
  scaleItem.setTitle("How ready do you feel to demonstrate and defend your component on Wednesday?")
           .setBounds(1, 5)
           .setLabels("Need Help / Alignment", "100% Prepared & Ready")
           .setRequired(true);

  // Open Notes / Blocker input
  var blockerItem = form.addParagraphTextItem();
  blockerItem.setTitle("Any blockers, questions, or areas where you need support before Wednesday?")
             .setRequired(false);

  // Log URLs
  var publishedUrl = form.getPublishedUrl();
  var editUrl = form.getEditUrl();

  Logger.log("\n=======================================================");
  Logger.log("✅ GOOGLE FORM CREATED SUCCESSFULLY!");
  Logger.log("=======================================================");
  Logger.log("📋 Public Shareable Link (Send to WhatsApp Group):");
  Logger.log(publishedUrl);
  Logger.log("\n✏️ Edit / Admin Link (View Responses & Form Settings):");
  Logger.log(editUrl);
  Logger.log("=======================================================\n");
}
