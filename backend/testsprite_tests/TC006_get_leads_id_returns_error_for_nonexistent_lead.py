import requests

BASE_URL = "http://localhost:5000"
TIMEOUT = 30

def test_get_lead_returns_error_for_nonexistent_lead():
    nonexistent_lead_id = "nonexistent-id-1234567890"
    url = f"{BASE_URL}/api/leads/{nonexistent_lead_id}"

    try:
        response = requests.get(url, timeout=TIMEOUT)
    except requests.RequestException as e:
        assert False, f"Request failed with exception: {e}"

    # Expecting an error response indicating lead not found, commonly 404
    assert response.status_code in [400, 404], (
        f"Expected 400 or 404 status code, got {response.status_code}. Response body: {response.text}"
    )

    # Attempt to verify response includes error indication
    try:
        data = response.json()
    except ValueError:
        assert False, "Response is not in JSON format"

    # The error response should have some message indicating lead was not found
    error_messages = [
        "not found",
        "not exist",
        "does not exist",
        "invalid",
        "error",
        "lead"
    ]
    error_text = str(data).lower()
    assert any(err in error_text for err in error_messages), (
        "Response JSON does not indicate lead not found or error. Response: " + str(data)
    )


test_get_lead_returns_error_for_nonexistent_lead()