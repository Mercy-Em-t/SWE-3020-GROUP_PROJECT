def test_full_member_savings_and_loan_journey(client):
    """
    End-to-End Integration User Journey covering:
    1. Member registration & authentication (FR-01)
    2. Savings deposit via M-Pesa (FR-02, FR-03)
    3. Checking borrowing limit (FR-04)
    4. Applying for loan with guarantor -> PENDING (FR-05, FR-06)
    5. Admin vetting and approval -> APPROVED (Admin Portal)
    6. Loan repayment (FR-07)
    7. Member directory listing (FR-08)
    8. Audit trail verification (FR-10)
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
    login_data = login_res.json()
    assert "access_token" in login_data
    token = login_data["access_token"]

    # Verify Profile via /auth/me
    me_res = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert me_res.status_code == 200
    assert me_res.json()["email"] == "mercy@sacco.test"

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
    assert loan_data["status"] == "PENDING"
    assert loan_data["principal_amount"] == 45000.0

    # 6. Admin checks pending loans queue
    pending_res = client.get("/api/v1/loans/pending")
    assert pending_res.status_code == 200
    pending_ids = [pl["id"] for pl in pending_res.json()]
    assert loan_id in pending_ids

    # 7. Admin vets and approves the loan
    vet_res = client.post(f"/api/v1/loans/{loan_id}/vet", json={
        "status": "APPROVED",
        "review_notes": "All guarantor commitments verified against shares."
    })
    assert vet_res.status_code == 200
    assert vet_res.json()["status"] == "APPROVED"

    # 8. Apply Loan Repayment
    repay_res = client.post("/api/v1/loans/repay", json={
        "loan_id": loan_id,
        "amount": 10000.0,
        "payment_reference": "MPESA_REPAY_001"
    })
    assert repay_res.status_code == 200
    repaid_data = repay_res.json()
    assert repaid_data["balance_outstanding"] == (
        loan_data["total_repayable"] - 10000.0
    )

    # 9. Admin checks member directory
    members_res = client.get("/api/v1/members")
    assert members_res.status_code == 200
    members_list = members_res.json()
    assert len(members_list) >= 2
    mercy_entry = next(
        m for m in members_list if m["email"] == "mercy@sacco.test"
    )
    assert mercy_entry["total_savings"] == 20000.0

    # 10. Verify Audit Trail Journal
    audit_res = client.get("/api/v1/audit/logs")
    assert audit_res.status_code == 200
    logs = audit_res.json()
    assert len(logs) >= 5
    actions = [log["action"] for log in logs]
    assert "MEMBER_REGISTERED" in actions
    assert "DEPOSIT_COMPLETED" in actions
    assert "LOAN_SUBMITTED" in actions
    assert "LOAN_APPROVED" in actions
    assert "LOAN_REPAYMENT_APPLIED" in actions
