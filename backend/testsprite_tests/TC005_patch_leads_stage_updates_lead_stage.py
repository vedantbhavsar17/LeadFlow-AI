import requests

BASE_URL = "http://localhost:5000"
TIMEOUT = 30


def test_patch_leads_stage_updates_lead_stage():
    # Create a new lead first to use in the patch test
    new_lead_payload = {
        "first_name": "Test",
        "last_name": "User",
        "email": "test.user@example.com",
        "company": "TestCompany"
    }

    lead_id = None
    try:
        # Create lead
        create_resp = requests.post(f"{BASE_URL}/api/leads", json=new_lead_payload, timeout=TIMEOUT)
        assert create_resp.status_code == 201, f"Expected 201 but got {create_resp.status_code}"
        create_data = create_resp.json()
        assert "lead" in create_data, "Response JSON does not contain 'lead'"
        lead = create_data["lead"]
        lead_id = lead.get("id")
        assert lead_id is not None, "Created lead does not contain 'id'"

        # Define new stage value (capitalized to align with typical stage naming)
        new_stage = "Qualification"

        # Patch lead stage
        patch_resp = requests.patch(
            f"{BASE_URL}/api/leads/{lead_id}/stage",
            json={"stage": new_stage},
            headers={"Content-Type": "application/json"},
            timeout=TIMEOUT
        )
        assert patch_resp.status_code == 200, f"Expected 200 but got {patch_resp.status_code}"
        patch_data = patch_resp.json()
        assert "lead" in patch_data, "PATCH response JSON does not contain 'lead'"
        updated_lead = patch_data["lead"]
        assert updated_lead.get("stage") == new_stage, f"Lead stage not updated in PATCH response. Expected '{new_stage}' got '{updated_lead.get('stage')}'"

        # Confirm lead stage update with GET
        get_resp = requests.get(f"{BASE_URL}/api/leads/{lead_id}", timeout=TIMEOUT)
        assert get_resp.status_code == 200, f"Expected 200 but got {get_resp.status_code}"
        get_data = get_resp.json()
        assert "lead" in get_data, "GET response JSON does not contain 'lead'"
        lead_from_get = get_data["lead"]
        assert lead_from_get.get("stage") == new_stage, f"Lead stage not updated in GET response. Expected '{new_stage}' got '{lead_from_get.get('stage')}'"

    finally:
        if lead_id:
            # Clean up by deleting the created lead if delete endpoint exists or ignore if not
            # Since delete endpoint is not provided in PRD, skipping explicit delete.
            pass


test_patch_leads_stage_updates_lead_stage()
