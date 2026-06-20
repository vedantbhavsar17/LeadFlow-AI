import requests

BASE_URL = "http://localhost:5000"
TIMEOUT = 30

def test_patch_leads_status_updates_lead_status():
    # Step 1: Create a new lead to use for testing the PATCH status update
    create_payload = {
        "first_name": "PatchTest",
        "last_name": "Lead",
        "email": "patchtest.lead@example.com",
        "company": "PatchTest Inc"
    }
    lead_id = None
    try:
        create_resp = requests.post(f"{BASE_URL}/api/leads", json=create_payload, timeout=TIMEOUT)
        assert create_resp.status_code == 201, f"Lead creation failed with status code {create_resp.status_code}"
        lead = create_resp.json().get("lead")
        assert lead and "id" in lead, "Response JSON missing 'lead.id'"
        lead_id = lead["id"]

        # Step 2: Patch the lead's status with a valid status value
        patch_payload = {"status": "qualified"}
        patch_resp = requests.patch(f"{BASE_URL}/api/leads/{lead_id}/status", json=patch_payload, timeout=TIMEOUT)
        assert patch_resp.status_code == 200, f"PATCH status update failed with status code {patch_resp.status_code}"
        patched_lead = patch_resp.json().get("lead")
        assert patched_lead and patched_lead.get("status") == patch_payload["status"], "Lead status not updated correctly in PATCH response"

        # Step 3: Confirm the lead's status via GET /api/leads/<id>
        get_resp = requests.get(f"{BASE_URL}/api/leads/{lead_id}", timeout=TIMEOUT)
        assert get_resp.status_code == 200, f"GET lead by id failed with status code {get_resp.status_code}"
        lead_after_patch = get_resp.json().get("lead")
        assert lead_after_patch and lead_after_patch.get("status") == patch_payload["status"], "Lead status not updated correctly in GET response after PATCH"

    finally:
        # Cleanup: Delete the created lead if possible (assuming DELETE /api/leads/<id> exists)
        if lead_id:
            try:
                requests.delete(f"{BASE_URL}/api/leads/{lead_id}", timeout=TIMEOUT)
            except Exception:
                # Ignore cleanup errors
                pass

test_patch_leads_status_updates_lead_status()