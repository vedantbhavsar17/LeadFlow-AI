import requests

BASE_URL = "http://localhost:5000"
TIMEOUT = 30

def test_get_leads_id_followups_returns_followup_tasks():
    lead_id = None
    created_lead = None
    
    # Create a new lead to use for followups retrieval
    try:
        create_lead_payload = {
            "first_name": "Test",
            "last_name": "User",
            "email": "test.user@example.com",
            "company": "TestCompany"
        }
        create_response = requests.post(f"{BASE_URL}/api/leads", json=create_lead_payload, timeout=TIMEOUT)
        assert create_response.status_code == 201, f"Expected status 201 but got {create_response.status_code}"
        created_lead = create_response.json().get("lead")
        assert created_lead is not None, "Response JSON does not contain 'lead'"
        lead_id = created_lead.get("id")
        assert lead_id is not None, "Created lead does not have an 'id'"

        # Request followups for this lead
        followups_response = requests.get(f"{BASE_URL}/api/leads/{lead_id}/followups", timeout=TIMEOUT)
        assert followups_response.status_code == 200, f"Expected status 200 but got {followups_response.status_code}"
        json_data = followups_response.json()
        assert "followups" in json_data, "'followups' key not in response JSON"
        assert isinstance(json_data["followups"], list), "'followups' is not a list"

    finally:
        # Clean up - delete the lead if created 
        if lead_id is not None:
            try:
                requests.delete(f"{BASE_URL}/api/leads/{lead_id}", timeout=TIMEOUT)
            except Exception:
                pass

test_get_leads_id_followups_returns_followup_tasks()