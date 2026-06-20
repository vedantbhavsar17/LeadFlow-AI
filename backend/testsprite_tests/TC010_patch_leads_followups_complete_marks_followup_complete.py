import requests

BASE_URL = "http://localhost:5000"
TIMEOUT = 30


def test_patch_leads_followups_complete_marks_followup_complete():
    # Step 1: Create a lead to associate the followup task
    lead_payload = {
        "first_name": "Test",
        "last_name": "User",
        "email": "testuser_patch_complete@example.com",
        "company": "TestCorp"
    }
    lead_resp = requests.post(f"{BASE_URL}/api/leads", json=lead_payload, timeout=TIMEOUT)
    assert lead_resp.status_code == 201, f"Lead creation failed: {lead_resp.text}"
    lead = lead_resp.json().get("lead")
    assert lead and "id" in lead, "Lead creation response does not contain id"
    lead_id = lead["id"]

    # Step 2: Create a follow-up task for this lead
    followup_payload = {
        "title": "Follow-up Test Task",
        "due_date": "2026-12-31T23:59:59Z",
        "notes": "This is a test followup."
    }
    followup_resp = requests.post(f"{BASE_URL}/api/leads/{lead_id}/followups", json=followup_payload, timeout=TIMEOUT)
    assert followup_resp.status_code == 201, f"Follow-up creation failed: {followup_resp.text}"
    followup = followup_resp.json().get("followup")
    assert followup and "id" in followup, "Follow-up creation response does not contain id"
    followup_id = followup["id"]

    try:
        # Step 3: Mark the follow-up task as complete using PATCH
        patch_resp = requests.patch(f"{BASE_URL}/api/leads/followups/{followup_id}/complete", timeout=TIMEOUT)
        assert patch_resp.status_code == 200, f"PATCH to complete follow-up failed: {patch_resp.text}"
        resp_json = patch_resp.json()
        completed_followup = resp_json.get("followup")
        assert completed_followup, "Response does not contain followup object"
        assert completed_followup.get("id") == followup_id, "Returned followup id mismatch"
        assert completed_followup.get("status") == "completed", "Followup status was not updated to completed"
    finally:
        # Cleanup: delete the follow-up task and the lead to keep test environment clean
        # Assuming DELETE endpoints exist for cleanup
        try:
            requests.delete(f"{BASE_URL}/api/leads/followups/{followup_id}", timeout=TIMEOUT)
        except Exception:
            pass
        try:
            requests.delete(f"{BASE_URL}/api/leads/{lead_id}", timeout=TIMEOUT)
        except Exception:
            pass

test_patch_leads_followups_complete_marks_followup_complete()