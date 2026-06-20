import requests

BASE_URL = "http://localhost:5000"
HEADERS = {"Content-Type": "application/json"}
TIMEOUT = 30

def test_put_leads_updates_existing_lead():
    # Create a new lead to update
    create_payload = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "company": "Doe Inc"
    }
    lead_id = None
    try:
        create_response = requests.post(
            f"{BASE_URL}/api/leads",
            json=create_payload,
            headers=HEADERS,
            timeout=TIMEOUT
        )
        assert create_response.status_code == 201, f"Expected status 201, got {create_response.status_code}"
        created_lead = create_response.json().get("lead")
        assert created_lead is not None, "Response JSON missing 'lead'"
        lead_id = created_lead.get("id")
        assert lead_id is not None, "Created lead missing 'id'"

        # Prepare updated data
        update_payload = {
            "first_name": "Jane",
            "last_name": "Smith",
            "email": "jane.smith@example.org",
            "company": "Smith LLC"
        }

        # Update the lead
        update_response = requests.put(
            f"{BASE_URL}/api/leads/{lead_id}",
            json=update_payload,
            headers=HEADERS,
            timeout=TIMEOUT
        )
        assert update_response.status_code == 200, f"Expected status 200, got {update_response.status_code}"
        updated_lead = update_response.json().get("lead")
        assert updated_lead is not None, "Response JSON missing 'lead'"
        # Assert updated fields
        assert updated_lead.get("first_name") == update_payload["first_name"], "First name not updated"
        assert updated_lead.get("last_name") == update_payload["last_name"], "Last name not updated"
        assert updated_lead.get("email") == update_payload["email"], "Email not updated"
        assert updated_lead.get("company") == update_payload["company"], "Company not updated"

        # Verify via GET that data is updated
        get_response = requests.get(
            f"{BASE_URL}/api/leads/{lead_id}",
            headers=HEADERS,
            timeout=TIMEOUT
        )
        assert get_response.status_code == 200, f"Expected status 200, got {get_response.status_code}"
        lead_after_update = get_response.json().get("lead")
        assert lead_after_update is not None, "Response JSON missing 'lead'"
        assert lead_after_update.get("first_name") == update_payload["first_name"], "GET first name does not match updated"
        assert lead_after_update.get("last_name") == update_payload["last_name"], "GET last name does not match updated"
        assert lead_after_update.get("email") == update_payload["email"], "GET email does not match updated"
        assert lead_after_update.get("company") == update_payload["company"], "GET company does not match updated"

    finally:
        # Cleanup: delete the created lead if exists
        if lead_id:
            try:
                requests.delete(f"{BASE_URL}/api/leads/{lead_id}", timeout=TIMEOUT)
            except Exception:
                pass

test_put_leads_updates_existing_lead()