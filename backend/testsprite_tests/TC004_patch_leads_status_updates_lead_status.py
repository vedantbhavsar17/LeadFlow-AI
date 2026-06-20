import requests

BASE_URL = "http://localhost:5000"
TIMEOUT = 30


def test_patch_leads_status_updates_lead_status():
    lead_data = {
        "first_name": "Test",
        "last_name": "User",
        "email": "test.user@example.com",
        "company": "TestCompany"
    }
    headers = {
        "Content-Type": "application/json"
    }
    lead_id = None
    try:
        # Create a new lead
        response_post = requests.post(f"{BASE_URL}/api/leads", json=lead_data, headers=headers, timeout=TIMEOUT)
        assert response_post.status_code == 201, f"Expected 201, got {response_post.status_code}"
        lead_id = response_post.json().get("lead", {}).get("id")
        assert lead_id is not None, "Lead ID not found in post response"

        # Patch lead status
        new_status = "Contacted"
        patch_payload = {"status": new_status}
        response_patch = requests.patch(f"{BASE_URL}/api/leads/{lead_id}/status", json=patch_payload, headers=headers, timeout=TIMEOUT)
        assert response_patch.status_code == 200, f"Expected 200, got {response_patch.status_code}"
        patched_lead = response_patch.json().get("lead")
        assert patched_lead is not None, "Lead object missing in patch response"
        assert patched_lead.get("status") == new_status, f"Lead status not updated in patch response (expected {new_status})"

        # Confirm via GET
        response_get = requests.get(f"{BASE_URL}/api/leads/{lead_id}", headers=headers, timeout=TIMEOUT)
        assert response_get.status_code == 200, f"Expected 200, got {response_get.status_code}"
        lead_get = response_get.json().get("lead")
        assert lead_get is not None, "Lead object missing in get response"
        assert lead_get.get("status") == new_status, f"Lead status not updated on get (expected {new_status})"
    finally:
        # Cleanup - delete the lead if created
        if lead_id:
            try:
                requests.delete(f"{BASE_URL}/api/leads/{lead_id}", timeout=TIMEOUT)
            except Exception:
                pass


test_patch_leads_status_updates_lead_status()