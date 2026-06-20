import requests

BASE_URL = "http://localhost:5000"
TIMEOUT = 30

def test_post_leads_creates_new_lead():
    lead_data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "company": "ExampleCorp"
    }
    headers = {
        "Content-Type": "application/json"
    }
    lead_id = None
    try:
        # Create a new lead
        post_response = requests.post(f"{BASE_URL}/api/leads", json=lead_data, headers=headers, timeout=TIMEOUT)
        assert post_response.status_code == 201, f"Expected status 201 but got {post_response.status_code}"
        post_json = post_response.json()
        assert "lead" in post_json, "Response JSON does not contain 'lead'"
        lead = post_json["lead"]
        for key in lead_data:
            assert lead.get(key) == lead_data[key], f"Lead {key} does not match input data"
        lead_id = lead.get("id")
        assert lead_id is not None, "Created lead does not have 'id'"

        # Retrieve the lead by ID to verify
        get_response = requests.get(f"{BASE_URL}/api/leads/{lead_id}", timeout=TIMEOUT)
        assert get_response.status_code == 200, f"Expected status 200 but got {get_response.status_code}"
        get_json = get_response.json()
        assert "lead" in get_json, "GET response JSON does not contain 'lead'"
        retrieved_lead = get_json["lead"]
        for key in lead_data:
            assert retrieved_lead.get(key) == lead_data[key], f"Retrieved lead {key} does not match input data"
        assert retrieved_lead.get("id") == lead_id, "Retrieved lead id does not match created lead id"
    finally:
        # Clean up: delete the created lead if it was created
        if lead_id is not None:
            requests.delete(f"{BASE_URL}/api/leads/{lead_id}", timeout=TIMEOUT)

test_post_leads_creates_new_lead()