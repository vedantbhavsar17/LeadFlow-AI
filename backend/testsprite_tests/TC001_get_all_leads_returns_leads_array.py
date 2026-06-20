import requests

BASE_URL = "http://localhost:5000"

def test_get_all_leads_returns_leads_array():
    url = f"{BASE_URL}/api/leads"
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
    except requests.RequestException as e:
        assert False, f"Request failed: {e}"

    assert response.status_code == 200, f"Expected status code 200 but got {response.status_code}"
    json_data = response.json()
    assert "leads" in json_data, "Response JSON does not contain 'leads' key"
    assert isinstance(json_data["leads"], list), "'leads' is not a list"

test_get_all_leads_returns_leads_array()