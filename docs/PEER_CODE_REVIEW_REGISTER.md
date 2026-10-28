# Peer Code Review & Formal Inspection Register

**Course:** SWE3020B – Software Quality Assurance and Security  
**Institution:** United States International University - Africa (USIU-Africa)  
**Governing Standard:** IEEE 1028-2008 (Standard for Software Reviews and Audits)  
**Deliverable:** CAT 2 Teamwork & Version Control Evaluation (30 Marks)  

---

## 1. Overview & Policy
In accordance with our project's Software Quality Assurance Plan (Section 3.1: *Source Control Governance & Code Review Policy*), no feature branch may merge into `develop` or `main` without undergoing an independent peer inspection. Code reviews focus on:
1. **Defensive Coding & Boundary Correctness**
2. **Runtime Exceptions & ReferenceErrors**
3. **Role-Based Security Invariants & Leakage**
4. **Adherence to Architectural Guidelines**

---

## 2. Formal Review Record: Pull Request #1

### Review Metadata
* **Pull Request:** PR #1 – `feat(frontend): scaffold React app with Vite`
* **Target Branch:** `develop` $\longleftarrow$ `feature/frontend`
* **Author:** Nyeliep Nial (`gielpalnyeliep@gmail.com`) – *UI/UX & Frontend Lead*
* **Lead Reviewer:** Mercy Tryphen (`memurugat@gmail.com`) – *System Architect & Backend Lead*
* **Inspection Date:** 2026-10-26
* **Verdict:** Approved with Required Patch (Non-blocking bug identified)

---

### Defect Finding Details

| Defect ID | Target File & Line | Severity | Classification | Defect Description |
| :--- | :--- | :---: | :---: | :--- |
| **REV-PR01-01** | `frontend/src/routes/ProtectedRoute.jsx:3-5` | **HIGH** | Runtime Scope / ReferenceError | Unbound variable `role` referenced in guard condition without destructuring in function parameter list. |

#### Detailed Defect Analysis:
* **The Code Submitted:**
  ```javascript
  // Line 3: Function only destructures 'children'
  export default function ProtectedRoute({ children }) {
      const user = JSON.parse(localStorage.getItem("user") || "null")
      if (!user) return <Navigate to="/login" replace={true} />
      
      // Line 5: 'role' is evaluated but does NOT exist in lexical scope!
      if (role && user.role !== role) return <Navigate to="/unauthorized" replace={true} />
      return children
  }
  ```

* **Root Cause & Impact:**
  * When a caller wraps an administrative page (e.g. `<ProtectedRoute role="treasurer"><Dashboard /></ProtectedRoute>`), JavaScript will evaluate `role` on Line 5.
  * Because `role` was never declared in the function arguments `({ children })`, JavaScript throws an uncaught **`ReferenceError: role is not defined`**, immediately crashing the React component tree and resulting in a blank White Screen of Death for users.

* **Required Remediation (The Fix):**
  Destructure `role` explicitly alongside `children` in the component prop signature:
  ```javascript
  export default function ProtectedRoute({ children, role }) {
      const user = JSON.parse(localStorage.getItem("user") || "null");
      if (!user) return <Navigate to="/login" replace={true} />;
      if (role && user.role !== role) return <Navigate to="/unauthorized" replace={true} />;
      return children;
  }
  ```

---

## 3. Ready-to-Paste GitHub PR Review Comment

Copy and paste this comment directly onto the GitHub Pull Request conversation:

```markdown
### 🔍 Peer Code Review Feedback — Mercy Tryphen (Lead Architect)

Hey @Nyeliep, great work on scaffolding the React + Vite frontend and setting up the reverse proxy to `:8000`! 🚀

During inspection of your security guards, I spotted one high-priority fix in `frontend/src/routes/ProtectedRoute.jsx`:

#### ⚠️ Runtime ReferenceError in `ProtectedRoute.jsx`
* **Location:** Lines 3 & 5
* **Issue:** Line 5 evaluates `if (role && user.role !== role)`, but `role` is not destructured in the function parameters on Line 3 (`{ children }`).
* **Impact:** Any component invoking `<ProtectedRoute role="treasurer">` will crash at runtime with `Uncaught ReferenceError: role is not defined`.
* **Fix:** Please update line 3 to destructure `role`:
  ```javascript
  export default function ProtectedRoute({ children, role }) {
  ```

Other than this prop destructuring, the reverse proxy configuration and API client look solid and connect seamlessly with our FastAPI backend endpoints. Approved pending this fix! 👍
```

---

## 4. Evaluation Defense Talking Point (Wednesday Presentation)

When presenting on **Slide 10 (*DevOps, Version Control & CI/CD*)** and **Slide 11 (*Team Collaboration & Project Management*)**:

> *"Our team enforced disciplined code review policies rather than just merging code blindly. For example, during the review of Pull Request #1 for the frontend scaffold, our lead engineer identified a runtime scope bug in `ProtectedRoute.jsx` where the `role` prop wasn't destructured, which would have thrown a `ReferenceError` on all administrative routes. Catching and resolving this during peer review prevented a production crash before the code ever reached `develop`."*
