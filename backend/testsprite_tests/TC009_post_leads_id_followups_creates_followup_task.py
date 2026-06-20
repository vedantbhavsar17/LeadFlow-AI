import requests

BASE_URL = "http://localhost:5000"
TIMEOUT = 30

def test_post_leads_id_followups_creates_followup_task():
    # Helper to create a lead
    def create_lead():
        lead_data = {
            "first_name": "Test",
            "last_name": "User",
            "email": "test.user@example.com",
            "company": "Test Company"
        }
        resp = requests.post(f"{BASE_URL}/api/leads", json=lead_data, timeout=TIMEOUT)
        resp.raise_for_status()
        assert resp.status_code == 201
        return resp.json()["lead"]["id"]

    # Helper to delete a lead (cleanup)
    def delete_lead(lead_id):
        # Assuming the API supports DELETE /api/leads/<id> to delete a lead (not specified in PRD)
        # If not available, skip cleanup.
        try:
            requests.delete(f"{BASE_URL}/api/leads/{lead_id}", timeout=TIMEOUT)
        except Exception:
            pass  # ignore cleanup errors

    lead_id = None
    followup_id = None
    try:
        # Create a lead if no id provided
        lead_id = create_lead()

        # Define follow-up task details
        followup_data = {
            "title": "Follow up call",
            "description": "Call to discuss product details",
            "due_date": "2026-07-01T10:00:00Z"
        }

        # POST /api/leads/<id>/followups to create a followup
        post_resp = requests.post(f"{BASE_URL}/api/leads/{lead_id}/followups", json=followup_data, timeout=TIMEOUT)
        assert post_resp.status_code == 201
        post_json = post_resp.json()
        assert "followup" in post_json
        followup = post_json["followup"]
        assert followup.get("id") is not None
        followup_id = followup.get("id")
        assert followup.get("title") == followup_data["title"]
        assert followup.get("description") == followup_data["description"]

        # GET /api/leads/<id>/followups to verify new followup appears
        get_resp = requests.get(f"{BASE_URL}/api/leads/{lead_id}/followups", timeout=TIMEOUT)
        assert get_resp.status_code == 200
        get_json = get_resp.json()
        assert "followups" in get_json
        followups = get_json["followups"]
        # The new followup task should appear in the followups list
        matched = [f for f in followups if f.get("id") == followup_id]
        assert len(matched) == 1
        matched_followup = matched[0]
        assert matched_followup.get("title") == followup_data["title"]
        assert matched_followup.get("description") == followup_data["description"]
    finally:
        # Cleanup: delete the lead (which also removes followups)
        if lead_id:
            delete_lead(lead_id)


test_post_leads_id_followups_creates_followup_task()
