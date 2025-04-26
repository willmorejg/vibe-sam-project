import pytest
from fastapi.testclient import TestClient
from fastapi import status
import uuid

from app.main import app
from app.routers.components import components_db

client = TestClient(app)

@pytest.fixture
def clear_db():
    # Clear the database before and after each test
    components_db.clear()
    yield
    components_db.clear()

def test_delete_component_not_found(clear_db):
    # Try to delete a component that doesn't exist
    random_id = str(uuid.uuid4())
    response = client.delete(f"/components/{random_id}")
    
    # Should return 404 Not Found
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "Component not found" in response.json()["detail"]

def test_delete_component_success(clear_db):
    # First create a component
    component_data = {
        "name": "Test Component",
        "description": "A test component"
    }
    
    # Create the component
    create_response = client.post("/components/", json=component_data)
    assert create_response.status_code == status.HTTP_201_CREATED
    
    # Get the component ID
    component_id = create_response.json()["id"]
    
    # Verify component exists
    get_response = client.get(f"/components/{component_id}")
    assert get_response.status_code == status.HTTP_200_OK
    
    # Delete the component
    delete_response = client.delete(f"/components/{component_id}")
    assert delete_response.status_code == status.HTTP_204_NO_CONTENT
    
    # Verify component no longer exists
    get_after_delete = client.get(f"/components/{component_id}")
    assert get_after_delete.status_code == status.HTTP_404_NOT_FOUND

def test_create_read_component(clear_db):
    # Test creating and reading a component
    component_data = {
        "name": "Another Component",
        "description": "Another test component",
        "properties": {"key": "value"}
    }
    
    # Create the component
    create_response = client.post("/components/", json=component_data)
    assert create_response.status_code == status.HTTP_201_CREATED
    created = create_response.json()
    
    # Verify data
    assert created["name"] == component_data["name"]
    assert created["description"] == component_data["description"]
    assert created["properties"] == component_data["properties"]
    
    # Get the component by ID
    component_id = created["id"]
    get_response = client.get(f"/components/{component_id}")
    assert get_response.status_code == status.HTTP_200_OK
    assert get_response.json() == created
