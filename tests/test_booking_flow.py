import pytest
from fastapi.testclient import TestClient
from app.main import app
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

client = TestClient(app)

# Test setup
PROVIDER = {
    "name": "Provider0",
    "email": "provider0@example.com",
    "password": "test1234",
    "role": "provider"
}
CUSTOMER = {
    "name": "Customer0",
    "email": "customer0@example.com",
    "password": "test1234",
    "role": "customer"
}

@pytest.fixture(scope="module")
def provider_token():
    client.post("/auth/register", json=PROVIDER)
    res = client.post("/auth/login", json=PROVIDER)
    return res.json()["access_token"]

@pytest.fixture(scope="module")
def customer_token():
    client.post("/auth/register", json=CUSTOMER)
    res = client.post("/auth/login", json=CUSTOMER)
    return res.json()["access_token"]

@pytest.fixture(scope="module")
def service_id(provider_token):
    res = client.post("/services", headers={"Authorization": f"Bearer {provider_token}"}, json={
        "name": "Haircut",
        "description": "Basic cut",
        "duration_minutes": 30,
        "price_cents": 2000
    })
    return res.json()["id"]

@pytest.fixture(scope="module")
def availability(provider_token):
    res = client.post("/availability", headers={"Authorization": f"Bearer {provider_token}"}, json={
        "day_of_week": 6,
        "start_time": "09:00:00",
        "end_time": "12:00:00"
    })
    return res.json()

def test_booking_creation_and_overlap(provider_token, customer_token, service_id):
    # Get provider UUID from service
    service = client.get(f"/services/{service_id}", headers={"Authorization": f"Bearer {provider_token}"}).json()
    provider_id = service["provider_id"]

    # Book a slot
    booking_payload = {
        "provider_id": provider_id,
        "service_id": service_id,
        "start_time": "2025-06-08T10:00:00",
        "end_time": "2025-06-08T10:30:00"
    }
    res1 = client.post("/bookings", headers={"Authorization": f"Bearer {customer_token}"}, json=booking_payload)
    assert res1.status_code == 200

    # Try overlapping booking
    res2 = client.post("/bookings", headers={"Authorization": f"Bearer {customer_token}"}, json=booking_payload)
    assert res2.status_code == 409  # conflict
