import requests

BASE_URL = "http://localhost:5000"
TIMEOUT = 30

def test_patch_leads_followups_complete_marks_followup_complete():
    # Step 1: Create a lead to associate a followup
    lead_payload = {
        "first_name": "Test",
        "last_name": "User",
        "email": "testuser@example.com",
        "company": "TestCompany"
    }
    lead_response = requests.post(f"{BASE_URL}/api/leads", json=lead_payload, timeout=TIMEOUT)
    assert lead_response.status_code == 201, f"Failed to create lead: {lead_response.text}"
    lead = lead_response.json().get("lead")
    assert lead and "id" in lead, "Lead ID missing in create response"
    lead_id = lead["id"]

    followup_id = None
    try:
        # Step 2: Create a followup task for the lead
        followup_payload = {
            "title": "Test Followup Task",
            "due_date": None,
            "notes": "Followup notes."
        }
        create_followup_resp = requests.post(f"{BASE_URL}/api/leads/{lead_id}/followups", json=followup_payload, timeout=TIMEOUT)
        assert create_followup_resp.status_code == 201, f"Failed to create followup: {create_followup_resp.text}"
        followup = create_followup_resp.json().get("followup")
        assert followup and "id" in followup, "Followup ID missing in create response"
        followup_id = followup["id"]

        # Step 3: PATCH to mark the followup as complete
        patch_resp = requests.patch(f"{BASE_URL}/api/leads/followups/{followup_id}/complete", timeout=TIMEOUT)
        assert patch_resp.status_code == 200, f"Failed to complete followup: {patch_resp.text}"
        patched_followup = patch_resp.json().get("followup")
        assert patched_followup, "Response missing 'followup' data"
        # Validate that the followup status is marked complete, assuming a field 'completed' or 'status' indicates this
        # As PRD doesn't specify exact field, check for typical keys
        completed_status = patched_followup.get("completed") or patched_followup.get("status")
        assert completed_status in [True, "completed", "done", "completed"], "Followup not marked as completed"

    finally:
        # Cleanup: Delete the created followup and lead if delete endpoints exist. Since PRD does not mention delete,
        # skip actual deletion; in real tests, you might deactivate or handle cleanup differently.
        # Here at least attempt to mark as complete if not yet done or note as cleanup.
        pass

test_patch_leads_followups_complete_marks_followup_complete()