def test_register_and_login_flow(client):
    # 1. Register user
    reg_payload = {
        "email": "engineer@pulseops.io",
        "username": "lead_engineer",
        "password": "Secr3tP@ssword123",
        "full_name": "Kalyani Nemade",
        "role": "lead_engineer"
    }
    res = client.post("/api/v1/auth/register", json=reg_payload)
    assert res.status_code == 201
    data = res.json()
    assert data["username"] == "lead_engineer"
    assert data["email"] == "engineer@pulseops.io"
    
    # 2. Login to get JWT
    login_payload = {
        "username": "lead_engineer",
        "password": "Secr3tP@ssword123"
    }
    res_login = client.post("/api/v1/auth/login", data=login_payload)
    assert res_login.status_code == 200
    token_data = res_login.json()
    assert "access_token" in token_data
    assert token_data["token_type"] == "bearer"
    
    # 3. Access /me protected endpoint
    headers = {"Authorization": f"Bearer {token_data['access_token']}"}
    res_me = client.get("/api/v1/auth/me", headers=headers)
    assert res_me.status_code == 200
    assert res_me.json()['username'] == "lead_engineer"
