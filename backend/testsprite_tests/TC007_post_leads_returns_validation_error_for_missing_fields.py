import requests

BASE_URL = "http://localhost:5000"
TIMEOUT = 30

def test_post_leads_returns_validation_error_for_missing_fields():
    url = f"{BASE_URL}/api/leads"
    # Missing all required fields, empty payload
    payload = {}
    headers = {
        "Content-Type": "application/json"
    }
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=TIMEOUT)
    except requests.RequestException as e:
        assert False, f"Request failed: {e}"

    # Expecting 4xx status code indicating validation error (likely 400 Bad Request)
    assert response.status_code >= 400 and response.status_code < 500, \
        f"Expected client error status, got {response.status_code}"

    try:
        json_response = response.json()
    except ValueError:
        assert False, "Response is not valid JSON"

    # Validation error usually contains error messages or details about missing fields
    # Check that the response contains error information related to missing fields
    # We look for keys like 'error', 'errors', 'message', or similar
    assert any(key in json_response for key in ["error", "errors", "message"]), \
        f"Response JSON missing expected error keys: {json_response}"

test_post_leads_returns_validation_error_for_missing_fields()