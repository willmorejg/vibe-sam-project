import pytest
from fastapi.testclient import TestClient
from fastapi import status
import uuid

from app.main import app
from app.routers.systems import systems_db

client = TestClient(app)

@pytest.fixture
def clear_db():
    # Clear the database before and after each test
    systems_db.clear()
    yield
    systems_db.clear()

def test_delete_system_not_found(clear_db):
    # Try to delete a system that doesn't exist
    random_id = str(uuid.uuid4())
    response = client.delete(f"/systems/{random_id}")
    
    # Should return 404 Not Found
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "System not found" in response.json()["detail"]

def test_delete_system_success(clear_db):
    # First create a system
    system_data = {
        "name": "Test System",
        "description": "A test system"
    }
    
    # Create the system
    create_response = client.post("/systems/", json=system_data)
    assert create_response.status_code == status.HTTP_201_CREATED
    
    # Get the system ID
    system_id = create_response.json()["id"]
    
    # Verify system exists
    get_response = client.get(f"/systems/{system_id}")
    assert get_response.status_code == status.HTTP_200_OK
    
    # Delete the system
    delete_response = client.delete(f"/systems/{system_id}")
    assert delete_response.status_code == status.HTTP_204_NO_CONTENT
    
    # Verify system no longer exists
    get_after_delete = client.get(f"/systems/{system_id}")
    assert get_after_delete.status_code == status.HTTP_404_NOT_FOUND

def test_create_read_system(clear_db):
    # Test creating and reading a system
    system_data = {
        "name": "Another System",
        "description": "Another test system",
        "properties": {"key": "value"}
    }
    
    # Create the system
    create_response = client.post("/systems/", json=system_data)
    assert create_response.status_code == status.HTTP_201_CREATED
    created = create_response.json()
    
    # Verify data
    assert created["name"] == system_data["name"]
    assert created["description"] == system_data["description"]
    assert created["properties"] == system_data["properties"]
    
    # Get the system by ID
    system_id = created["id"]
    get_response = client.get(f"/systems/{system_id}")
    assert get_response.status_code == status.HTTP_200_OK
    assert get_response.json() == created
