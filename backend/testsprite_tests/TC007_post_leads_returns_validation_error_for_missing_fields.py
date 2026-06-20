import requests

BASE_URL = "http://localhost:5000"
TIMEOUT = 30

def test_post_leads_validation_error_missing_fields():
    url = f"{BASE_URL}/api/leads"
    # Prepare payload with missing required fields (empty payload)
    payload = {}
    headers = {
        "Content-Type": "application/json"
    }
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=TIMEOUT)
    except requests.RequestException as e:
        assert False, f"Request failed: {e}"

    # Expecting a validation error response (likely 400 Bad Request)
    assert response.status_code in (400, 422), f"Expected status 400 or 422, got {response.status_code}"
    try:
        data = response.json()
    except ValueError:
        assert False, "Response is not valid JSON"

    # Check that error info about missing fields is present in response
    # The exact structure is not given, so we check for typical keys
    assert "error" in data or "errors" in data or "message" in data, "Validation error details not found in response"

test_post_leads_validation_error_missing_fields()