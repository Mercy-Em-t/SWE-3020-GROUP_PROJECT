def test_full_member_savings_and_loan_journey(client):
    """
    End-to-End Integration User Journey covering:
    1. Member registration & authentication (FR-01)
    2. Savings deposit via M-Pesa (FR-02, FR-03)
    3. Checking borrowing limit (FR-04)
    4. Applying for loan with guarantor (FR-05, FR-06)
    5. Loan repayment (FR-07)
    6. Audit trail verification (FR-10)
    """
    # 1. Register Member
    reg_res = client.post("/api/v1/auth/register", json={
        "email": "mercy@sacco.test",
        "full_name": "Mercy Tryphen",
        "phone_number": "+254712345678",
        "password": "SecurePassword123!",
        "role": "member"
    })
    assert reg_res.status_code == 201
    member = reg_res.json()
    member_id = member["id"]

    # Register a guarantor member
    g_res = client.post("/api/v1/auth/register", json={
        "email": "guarantor@sacco.test",
        "full_name": "Jescah Guarantor",
        "phone_number": "+254798765432",
        "password": "SecurePassword123!",
        "role": "member"
    })
    assert g_res.status_code == 201
    guarantor_id = g_res.json()["id"]

    # 2. Login
    login_res = client.post("/api/v1/auth/login", json={
        "email": "mercy@sacco.test",
        "password": "SecurePassword123!"
    })
    assert login_res.status_code == 200
    assert "access_token" in login_res.json()

    # 3. Make Deposit (KES 20,000)
    dep_res = client.post("/api/v1/savings/deposit", json={
        "member_id": member_id,
        "amount": 20000.0,
        "phone_number": "+254712345678",
        "payment_channel": "mpesa"
    })
    assert dep_res.status_code == 200
    dep_data = dep_res.json()
    assert dep_data["success"] is True
    assert dep_data["new_savings_balance"] == 20000.0
    assert dep_data["new_total_shares"] == 20000.0

    # 4. Check Loan Eligibility (Limit should be 3x 20,000 = 60,000)
    elig_res = client.get(f"/api/v1/loans/eligibility/{member_id}")
    assert elig_res.status_code == 200
    elig_data = elig_res.json()
    assert elig_data["total_shares"] == 20000.0
    assert elig_data["max_borrowing_limit"] == 60000.0
    assert elig_data["is_eligible"] is True

    # 5. Apply for Loan: KES 45,000 for 12 months.
    # Uncollateralized delta = 45,000 - 20,000 = 25,000.
    # Guarantor commits KES 25,000.
    loan_apply_res = client.post("/api/v1/loans/apply", json={
        "member_id": member_id,
        "principal_amount": 45000.0,
        "duration_months": 12,
        "guarantors": [
            {
                "guarantor_member_id": guarantor_id,
                "amount_guaranteed": 25000.0
            }
        ]
    })
    assert loan_apply_res.status_code == 201
    loan_data = loan_apply_res.json()
    loan_id = loan_data["id"]
    assert loan_data["status"] == "APPROVED"
    assert loan_data["principal_amount"] == 45000.0
    assert loan_data["total_repayable"] > 45000.0

    # 6. Apply Loan Repayment
    repay_res = client.post("/api/v1/loans/repay", json={
        "loan_id": loan_id,
        "amount": 10000.0,
        "payment_reference": "MPESA_REPAY_001"
    })
    assert repay_res.status_code == 200
    repaid_data = repay_res.json()
    assert repaid_data["balance_outstanding"] == loan_data["total_repayable"] - 10000.0

    # 7. Verify Audit Trail Journal
    audit_res = client.get("/api/v1/audit/logs")
    assert audit_res.status_code == 200
    logs = audit_res.json()
    assert len(logs) >= 4
    actions = [log["action"] for log in logs]
    assert "MEMBER_REGISTERED" in actions
    assert "DEPOSIT_COMPLETED" in actions
    assert "LOAN_APPROVED" in actions
    assert "LOAN_REPAYMENT_APPLIED" in actions
