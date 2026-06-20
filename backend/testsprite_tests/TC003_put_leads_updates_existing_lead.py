import requests

BASE_URL = "http://localhost:5000"
TIMEOUT = 30

def test_put_leads_updates_existing_lead():
    # Step 1: Create a new lead to update
    create_payload = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "company": "Example Inc"
    }
    created_lead_id = None

    try:
        create_response = requests.post(
            f"{BASE_URL}/api/leads",
            json=create_payload,
            timeout=TIMEOUT
        )
        assert create_response.status_code == 201, f"Expected status 201, got {create_response.status_code}"
        created_lead = create_response.json().get("lead")
        assert created_lead is not None and "id" in created_lead, "Lead creation response missing 'id'"
        created_lead_id = created_lead["id"]

        # Step 2: Update the created lead with PUT
        update_payload = {
            "first_name": "Jane",
            "last_name": "Smith",
            "email": "jane.smith@example.com",
            "company": "New Example LLC"
        }
        put_response = requests.put(
            f"{BASE_URL}/api/leads/{created_lead_id}",
            json=update_payload,
            timeout=TIMEOUT
        )
        assert put_response.status_code == 200, f"Expected status 200, got {put_response.status_code}"
        updated_lead = put_response.json().get("lead")
        assert updated_lead is not None, "PUT response missing 'lead' data"
        for key in update_payload:
            assert updated_lead.get(key) == update_payload[key], f"Lead {key} not updated correctly"

        # Step 3: Verify update via GET
        get_response = requests.get(
            f"{BASE_URL}/api/leads/{created_lead_id}",
            timeout=TIMEOUT
        )
        assert get_response.status_code == 200, f"Expected status 200, got {get_response.status_code}"
        get_lead = get_response.json().get("lead")
        assert get_lead is not None, "GET response missing 'lead' data"
        for key in update_payload:
            assert get_lead.get(key) == update_payload[key], f"Lead {key} value incorrect on GET"

    finally:
        # Cleanup - delete the created lead
        if created_lead_id:
            try:
                requests.delete(
                    f"{BASE_URL}/api/leads/{created_lead_id}",
                    timeout=TIMEOUT
                )
            except Exception:
                pass

test_put_leads_updates_existing_lead()