# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     https://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Tests for the service layer using pytest."""

import pytest
from uuid import UUID

from archman.models import Component, System
from archman.services import ComponentService, SystemService

# Global variables to store IDs between tests
service_component_id = None
service_system_id = None
service_test_components = []

class TestComponentService:
    """Tests for the ComponentService."""
    
    @pytest.mark.dependency()
    def test_create_component(self):
        """Test creating a component through the service."""
        service = ComponentService()
        component = Component(
            name="Service Test Component",
            type="software",
            properties={"language": "Python"},
        )
        
        # Save the component UUID for next tests
        global service_component_id
        service_component_id = component.uuid
        
        # Create the component
        result = service.create_or_update(component)
        assert result.name == "Service Test Component"
        assert result.type == "software"
        assert result.properties == {"language": "Python"}
        
        # Verify it was created
        fetched = service.get(component.uuid)
        assert fetched is not None
        assert fetched.name == "Service Test Component"
        
        # Test get_all method
        all_components = service.get_all()
        assert len(all_components) >= 1
        component_uuids = [str(c.uuid) for c in all_components]
        assert str(component.uuid) in component_uuids
    
    @pytest.mark.dependency(depends=["TestComponentService::test_create_component"])
    def test_update_component(self):
        """Test updating a component through the service."""
        service = ComponentService()
        
        # Get the component
        global service_component_id
        component = service.get(service_component_id)
        assert component is not None
        
        # Update the component
        component.name = "Updated Service Component"
        component.properties["version"] = "2.0"
        result = service.create_or_update(component)
        
        # Verify the update
        assert result.name == "Updated Service Component"
        assert result.properties["version"] == "2.0"
        
        # Check that it was persisted
        fetched = service.get(service_component_id)
        assert fetched is not None
        assert fetched.name == "Updated Service Component"
        assert fetched.properties["version"] == "2.0"
        
        # Test get_by_type method
        components_by_type = service.get_by_type("software")
        assert len(components_by_type) >= 1
        assert any(c.name == "Updated Service Component" for c in components_by_type)
    
    @pytest.mark.dependency(depends=["TestComponentService::test_update_component"])
    def test_delete_component(self):
        """Test deleting a component through the service."""
        service = ComponentService()
        
        # Delete the component
        global service_component_id
        result = service.delete(service_component_id)
        assert result is True
        
        # Verify it was deleted
        fetched = service.get(service_component_id)
        assert fetched is None


class TestSystemService:
    """Tests for the SystemService."""
    
    @pytest.fixture
    def setup_service_components(self):
        """Create test components for system service tests."""
        service = ComponentService()
        comp1 = Component(name="System Service Test Component 1", type="software")
        comp2 = Component(name="System Service Test Component 2", type="hardware")
        service.create_or_update(comp1)
        service.create_or_update(comp2)
        
        global service_test_components
        service_test_components = [comp1, comp2]
        return [comp1, comp2]
    
    @pytest.mark.dependency()
    def test_create_system(self, setup_service_components):
        """Test creating a system through the service."""
        service = SystemService()
        
        # Get components from fixture
        components = setup_service_components
        
        system = System(
            name="Service Test System",
            components=[components[0].uuid, components[1].uuid],
            properties={"environment": "development"},
        )
        
        # Save the system UUID for next tests
        global service_system_id
        service_system_id = system.uuid
        
        # Create the system
        result = service.create_or_update(system)
        assert result.name == "Service Test System"
        
        # Verify it was created
        fetched = service.get(system.uuid)
        assert fetched is not None
        assert fetched.name == "Service Test System"
        assert len(fetched.components) == 2
    
    @pytest.mark.dependency(depends=["TestSystemService::test_create_system"])
    def test_get_full_system(self):
        """Test getting a full system with component details."""
        service = SystemService()
        
        # Get the full system with component details
        global service_system_id
        full_system = service.get_full_system(service_system_id)
        assert full_system is not None
        assert full_system.name == "Service Test System"
        
        # Verify components are loaded
        assert len(full_system.components) == 2
        
        # Check each component is either a Component object or has the expected UUID
        loaded_components = full_system.components
        for comp in loaded_components:
            if isinstance(comp, Component):
                assert comp.name.startswith("System Service Test Component")
            else:
                # It might be a UUID in some implementations
                assert str(comp) in [str(c.uuid) for c in service_test_components]
    
    @pytest.mark.dependency(depends=["TestSystemService::test_get_full_system"])
    def test_update_system(self):
        """Test updating a system through the service."""
        service = SystemService()
        
        # Get the system
        global service_system_id
        system = service.get(service_system_id)
        assert system is not None
        
        # Update the system
        system.name = "Updated Service System"
        system.properties["status"] = "active"
        result = service.create_or_update(system)
        
        # Verify the update
        assert result.name == "Updated Service System"
        assert result.properties["status"] == "active"
        
        # Check that it was persisted
        fetched = service.get(service_system_id)
        assert fetched is not None
        assert fetched.name == "Updated Service System"
        assert fetched.properties["status"] == "active"
    
    @pytest.mark.dependency(depends=["TestSystemService::test_update_system"])
    def test_add_remove_component(self):
        """Test adding and removing components from a system."""
        service = SystemService()
        comp_service = ComponentService()
        
        # Create a new component to add
        new_component = Component(name="New Test Component", type="database")
        comp_service.create_or_update(new_component)
        
        # Add the component to the system
        global service_system_id
        updated_system = service.add_component_to_system(
            service_system_id, new_component.uuid
        )
        assert updated_system is not None
        
        # Check the component was added
        fetched = service.get(service_system_id)
        component_uuids = [str(c) for c in fetched.components]
        assert str(new_component.uuid) in component_uuids
        
        # Remove the component
        updated_system = service.remove_component_from_system(
            service_system_id, new_component.uuid
        )
        assert updated_system is not None
        
        # Check the component was removed
        fetched = service.get(service_system_id)
        component_uuids = [str(c) for c in fetched.components]
        assert str(new_component.uuid) not in component_uuids
    
    @pytest.mark.dependency(depends=["TestSystemService::test_add_remove_component"])
    def test_delete_system(self):
        """Test deleting a system through the service."""
        service = SystemService()
        
        # Delete the system
        global service_system_id
        result = service.delete(service_system_id)
        assert result is True
        
        # Verify it was deleted
        fetched = service.get(service_system_id)
        assert fetched is None
