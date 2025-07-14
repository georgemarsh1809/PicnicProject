# Tests for FastAPI routes
from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)    

# Test Data
existing_code = "KYgrDJ"  # Ensure existing_code is in the urlCodes.json file
non_existing_code = "111111" # Ensure non_existing_code is NOT in the urlCodes.json file
valid_payload = {"url": "https://example.com"} # Ensure the URL is valid (as defined by AnyHttpUrl) AND NOT  in the urlCodes.json file
invalid_payload = {"url": "invalid_payload"}
empty_payload = {}
existing_url = "https://google.com/"  # Ensure the URL already exists in the urlCodes.json file

# Test cases for each endpoint and variations of payloads
#   'GET /{code}' tests
def test_get_code_with_valid_code():
    response = client.get(f"/{existing_code}")
    assert response.status_code == 200
    assert "longUrl" in response.json()

def test_get_code_with_invalid_code():
    response = client.get(f"/{non_existing_code}")
    assert response.status_code == 404
    assert response.json() == {"detail": "Shortened URL code not found"}

#   'POST /shorten/' tests
def test_shorten_url_with_valid_payload():
    response = client.post("/shorten/", json=valid_payload)
    assert response.status_code == 201

def test_shorten_url_with_invalid_payload():
    response = client.post("/shorten/", json=invalid_payload)
    assert response.status_code == 422
    assert response.json() == {"error": "Invalid URL format, ensure the URL starts with http:// or https://"}

def test_shorten_url_with_empty_payload():
    response = client.post("/shorten/", json=empty_payload)
    assert response.status_code == 422
    assert response.json() == {"error": "Invalid URL format, ensure the URL starts with http:// or https://"}
    
def test_shorten_url_with_existing_url():
    response = client.post("/shorten/", json={"url": existing_url})
    assert response.status_code == 409
    assert response.json() == {"error": f"Code already exists for this URL: {existing_url}"}



