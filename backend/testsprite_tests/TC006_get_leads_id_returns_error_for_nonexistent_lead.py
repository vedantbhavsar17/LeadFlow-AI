import requests

BASE_URL = "http://localhost:5000"
TIMEOUT = 30

def test_get_leads_id_returns_error_for_nonexistent_lead():
    non_existent_id = "00000000-0000-0000-0000-000000000000"
    url = f"{BASE_URL}/api/leads/{non_existent_id}"
    try:
        response = requests.get(url, timeout=TIMEOUT)
        # The API should return an error status code for non-existent lead.
        # We expect a 4xx, typically 404 Not Found.
        assert response.status_code in (400, 404), f"Expected 400 or 404, got {response.status_code}"
        
        # Response is expected to indicate the lead was not found.
        json_data = response.json()
        # The exact error response format isn't specified, check for common keys and messages
        assert isinstance(json_data, dict), "Response is not a JSON object"
        # Check for presence of error message or description
        error_found = False
        if "error" in json_data:
            error_found = True
            assert isinstance(json_data["error"], str) and len(json_data["error"]) > 0
        if "message" in json_data:
            error_found = True
            assert isinstance(json_data["message"], str) and "not found" in json_data["message"].lower()
        assert error_found, "Error message indicating lead not found is missing in response"
    except requests.RequestException as e:
        assert False, f"Request failed: {e}"

test_get_leads_id_returns_error_for_nonexistent_lead()