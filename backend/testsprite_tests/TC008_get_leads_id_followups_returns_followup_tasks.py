import requests

BASE_URL = "http://localhost:5000"
TIMEOUT = 30

def test_get_leads_id_followups_returns_followup_tasks():
    # Step 1: Create a new lead to get a valid lead ID for testing
    lead_data = {
        "first_name": "Test",
        "last_name": "User",
        "email": "testuser@example.com",
        "company": "Test Company"
    }
    lead = None
    try:
        create_lead_resp = requests.post(f"{BASE_URL}/api/leads", json=lead_data, timeout=TIMEOUT)
        assert create_lead_resp.status_code == 201, f"Expected 201 on lead creation but got {create_lead_resp.status_code}"
        lead = create_lead_resp.json().get("lead")
        assert lead is not None, "Lead data not returned in create response"
        lead_id = lead.get("id")
        assert lead_id is not None, "Lead ID missing in create response"

        # Step 2: Retrieve follow-up tasks for this lead (likely empty initially)
        get_followups_resp = requests.get(f"{BASE_URL}/api/leads/{lead_id}/followups", timeout=TIMEOUT)
        assert get_followups_resp.status_code == 200, f"Expected 200 on get followups but got {get_followups_resp.status_code}"
        
        followups_json = get_followups_resp.json()
        assert isinstance(followups_json, dict), "Response JSON is not a dict"
        assert "followups" in followups_json, "Response JSON missing 'followups' key"
        followups = followups_json["followups"]
        assert isinstance(followups, list), "'followups' is not a list"

    finally:
        # Clean up: delete the lead created for test
        if lead and lead_id:
            try:
                requests.delete(f"{BASE_URL}/api/leads/{lead_id}", timeout=TIMEOUT)
            except Exception:
                pass

test_get_leads_id_followups_returns_followup_tasks()