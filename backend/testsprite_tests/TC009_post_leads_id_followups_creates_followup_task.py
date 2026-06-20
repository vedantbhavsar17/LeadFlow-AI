import requests

BASE_URL = "http://localhost:5000"
TIMEOUT = 30

def test_post_leads_id_followups_creates_followup_task():
    lead_id = None
    followup_id = None
    try:
        # Step 1: Create a new lead to use for followup
        lead_payload = {
            "first_name": "Test",
            "last_name": "User",
            "email": "test.user@example.com",
            "company": "TestCompany"
        }
        lead_response = requests.post(f"{BASE_URL}/api/leads", json=lead_payload, timeout=TIMEOUT)
        assert lead_response.status_code == 201, f"Lead creation failed: {lead_response.text}"
        lead_data = lead_response.json()
        assert "lead" in lead_data and "id" in lead_data["lead"], "Lead ID missing in creation response"
        lead_id = lead_data["lead"]["id"]

        # Step 2: POST new follow-up task for the lead
        followup_payload = {
            "title": "Follow-up call",
            "due_date": "2026-07-01T10:00:00Z",
            "notes": "Call the lead to discuss product features."
        }
        # POST followup
        followup_response = requests.post(f"{BASE_URL}/api/leads/{lead_id}/followups", json=followup_payload, timeout=TIMEOUT)
        assert followup_response.status_code == 201, f"Followup creation failed: {followup_response.text}"
        followup_data = followup_response.json()
        assert "followup" in followup_data and "id" in followup_data["followup"], "Followup ID missing in creation response"
        followup_id = followup_data["followup"]["id"]

        # Step 3: GET followups to confirm new follow-up appears
        get_followups_response = requests.get(f"{BASE_URL}/api/leads/{lead_id}/followups", timeout=TIMEOUT)
        assert get_followups_response.status_code == 200, f"Failed to retrieve followups: {get_followups_response.text}"
        followups_list = get_followups_response.json().get("followups", [])
        # Check if the created followup task is in the list
        found_followup = any(f["id"] == followup_id for f in followups_list)
        assert found_followup, "Created follow-up task not found in followups list"

    finally:
        # Cleanup: delete created follow-up and lead if API supports DELETE (not specified in PRD, so ignore here)
        # If deletion endpoints existed, they would be called here.
        pass

test_post_leads_id_followups_creates_followup_task()