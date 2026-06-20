import requests

BASE_URL = "http://localhost:5000"
TIMEOUT = 30

def test_patch_leads_stage_updates_lead_stage():
    # Step 1: Create a new lead to update
    create_payload = {
        "first_name": "Test",
        "last_name": "User",
        "email": "testuser_stage_patch@example.com",
        "company": "TestCompany"
    }
    lead_id = None
    try:
        create_resp = requests.post(f"{BASE_URL}/api/leads", json=create_payload, timeout=TIMEOUT)
        assert create_resp.status_code == 201, f"Lead creation failed: {create_resp.text}"
        lead_data = create_resp.json().get("lead")
        assert lead_data and "id" in lead_data, "Response missing lead or lead id"
        lead_id = lead_data["id"]

        # Step 2: PATCH to update the lead stage
        patch_payload = {
            "stage": "Qualified"
        }
        patch_resp = requests.patch(f"{BASE_URL}/api/leads/{lead_id}/stage", json=patch_payload, timeout=TIMEOUT)
        assert patch_resp.status_code == 200, f"Patch stage failed: {patch_resp.text}"
        patched_lead = patch_resp.json().get("lead")
        assert patched_lead is not None, "Patch response missing lead"
        assert patched_lead.get("stage") == "Qualified", f"Lead stage not updated in patch response, got {patched_lead.get('stage')}"

        # Step 3: GET lead to confirm the stage update
        get_resp = requests.get(f"{BASE_URL}/api/leads/{lead_id}", timeout=TIMEOUT)
        assert get_resp.status_code == 200, f"Get lead failed: {get_resp.text}"
        get_lead = get_resp.json().get("lead")
        assert get_lead is not None, "Get response missing lead"
        assert get_lead.get("stage") == "Qualified", f"Lead stage not updated in get response, got {get_lead.get('stage')}"

    finally:
        # Cleanup - delete the lead created
        if lead_id:
            requests.delete(f"{BASE_URL}/api/leads/{lead_id}", timeout=TIMEOUT)

test_patch_leads_stage_updates_lead_stage()