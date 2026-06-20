import requests
import uuid

BASE_URL = "http://localhost:5000"
TIMEOUT = 30
HEADERS = {
    "Content-Type": "application/json"
}

def test_post_leads_creates_new_lead():
    lead_data = {
        "first_name": "TestFirstName",
        "last_name": "TestLastName",
        "email": f"testemail_{uuid.uuid4().hex[:8]}@example.com",
        "company": "TestCompany"
    }
    lead_id = None
    try:
        # Create a new lead with POST /api/leads
        post_response = requests.post(
            f"{BASE_URL}/api/leads",
            json=lead_data,
            headers=HEADERS,
            timeout=TIMEOUT
        )
        assert post_response.status_code == 201, f"Expected status 201, got {post_response.status_code}"
        post_response_json = post_response.json()
        assert "lead" in post_response_json, "Response JSON does not contain 'lead'"
        lead = post_response_json["lead"]
        # Validate returned lead fields match input
        assert lead.get("first_name") == lead_data["first_name"], "first_name mismatch"
        assert lead.get("last_name") == lead_data["last_name"], "last_name mismatch"
        assert lead.get("email") == lead_data["email"], "email mismatch"
        assert lead.get("company") == lead_data["company"], "company mismatch"
        assert "id" in lead, "Lead ID not present in response"
        lead_id = lead["id"]

        # Retrieve the lead with GET /api/leads/<id>
        get_response = requests.get(
            f"{BASE_URL}/api/leads/{lead_id}",
            headers=HEADERS,
            timeout=TIMEOUT
        )
        assert get_response.status_code == 200, f"Expected status 200, got {get_response.status_code}"
        get_response_json = get_response.json()
        assert "lead" in get_response_json, "Response JSON does not contain 'lead' on GET"
        retrieved_lead = get_response_json["lead"]
        # Validate retrieved lead fields
        assert retrieved_lead.get("id") == lead_id, "Lead ID mismatch on GET"
        assert retrieved_lead.get("first_name") == lead_data["first_name"], "first_name mismatch on GET"
        assert retrieved_lead.get("last_name") == lead_data["last_name"], "last_name mismatch on GET"
        assert retrieved_lead.get("email") == lead_data["email"], "email mismatch on GET"
        assert retrieved_lead.get("company") == lead_data["company"], "company mismatch on GET"

    finally:
        # Cleanup: Delete the created lead to maintain test environment
        if lead_id:
            try:
                requests.delete(
                    f"{BASE_URL}/api/leads/{lead_id}",
                    headers=HEADERS,
                    timeout=TIMEOUT
                )
            except Exception:
                pass

test_post_leads_creates_new_lead()