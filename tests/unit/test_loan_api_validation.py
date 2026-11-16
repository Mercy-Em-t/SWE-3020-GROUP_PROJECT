def test_loan_application_exceeding_borrowing_limit_rejected(client):
    """FR-04 & FR-05: Applying for loan > 3x shares must return 400 Bad Request."""
    # 1. Register & Login
    reg = client.post("/api/v1/auth/register", json={
        "email": "borrower_limit@sacco.test",
        "full_name": "Over Borrower",
        "phone_number": "+254700000001",
        "password": "Password123"
    })
    member_id = reg.json()["id"]

    login = client.post("/api/v1/auth/login", json={
        "email": "borrower_limit@sacco.test",
        "password": "Password123"
    })
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Deposit KES 10,000 (Max borrowing limit = KES 30,000)
    client.post(
        "/api/v1/savings/deposit",
        json={
            "member_id": member_id,
            "amount": 10000.0,
            "phone_number": "+254700000001"
        },
        headers=headers
    )

    # 3. Attempt to borrow KES 50,000 (exceeds KES 30,000 limit)
    res = client.post(
        "/api/v1/loans/apply",
        json={
            "member_id": member_id,
            "principal_amount": 50000.0,
            "duration_months": 12,
            "guarantors": []
        },
        headers=headers
    )
    assert res.status_code == 400
    assert "exceeds allowable limit" in res.json()["detail"]


def test_loan_application_insufficient_guarantors_rejected(client):
    """FR-06: Loan within limit but without sufficient guarantor coverage must return 400."""
    # 1. Register & Login
    reg = client.post("/api/v1/auth/register", json={
        "email": "guarantor_fail@sacco.test",
        "full_name": "Guarantor Fail",
        "phone_number": "+254700000002",
        "password": "Password123"
    })
    member_id = reg.json()["id"]

    login = client.post("/api/v1/auth/login", json={
        "email": "guarantor_fail@sacco.test",
        "password": "Password123"
    })
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Deposit KES 10,000 (Max limit = KES 30,000)
    client.post(
        "/api/v1/savings/deposit",
        json={
            "member_id": member_id,
            "amount": 10000.0,
            "phone_number": "+254700000002"
        },
        headers=headers
    )

    # 3. Borrow KES 25,000 (Uncollateralized portion = 25k - 10k = 15k)
    # Provide only 5k in guarantor guarantee
    res = client.post(
        "/api/v1/loans/apply",
        json={
            "member_id": member_id,
            "principal_amount": 25000.0,
            "duration_months": 6,
            "guarantors": [
                {
                    "guarantor_member_id": 999,
                    "amount_guaranteed": 5000.0
                }
            ]
        },
        headers=headers
    )
    assert res.status_code == 400
