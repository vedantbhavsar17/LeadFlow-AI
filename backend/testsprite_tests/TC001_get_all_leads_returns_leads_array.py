import requests

BASE_URL = "http://localhost:5000"
TIMEOUT = 30

def test_get_all_leads_returns_leads_array():
    url = f"{BASE_URL}/api/leads"
    try:
        response = requests.get(url, timeout=TIMEOUT)
        assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
        data = response.json()
        assert "leads" in data, "'leads' key not found in response"
        assert isinstance(data["leads"], list), f"'leads' should be a list but got {type(data['leads'])}"
    except requests.RequestException as e:
        assert False, f"Request failed: {e}"

test_get_all_leads_returns_leads_array()