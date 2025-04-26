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

import pytest
from uuid import UUID

from archman.models import Component, System
from archman.repositories import ComponentRepository, SystemRepository

# Global variables to store IDs between tests
component_id = None
system_id = None
system_components = []

class TestComponentRepository:
    """Tests for the ComponentRepository."""
    
    @pytest.mark.dependency()
    def test_create_component(self):
        """Test creating a component."""
        repo = ComponentRepository()
        component = Component(
            name="Test Component",
            type="software",
            properties={"language": "Python"},
        )
        
        # Create the component
        result = repo.upsert(component)
        assert result.name == "Test Component"
        assert result.type == "software"
        assert result.properties == {"language": "Python"}
        
        # Save the component UUID for next tests
        global component_id
        component_id = result.uuid
        
        # Verify it was created
        fetched = repo.get_by_id(result.uuid)
        assert fetched is not None
        assert fetched.name == "Test Component"
    
    @pytest.mark.dependency(depends=["TestComponentRepository::test_create_component"])
    def test_update_component(self):
        """Test updating a component."""
        repo = ComponentRepository()
        
        # Get the component
        global component_id
        component = repo.get_by_id(component_id)
        assert component is not None
        
        # Update the component
        component.name = "Updated Component"
        component.properties["version"] = "2.0"
        result = repo.upsert(component)
        
        # Verify the update
        assert result.name == "Updated Component"
        assert result.properties["version"] == "2.0"
        
        # Check that it was persisted
        fetched = repo.get_by_id(component_id)
        assert fetched is not None
        assert fetched.name == "Updated Component"
        assert fetched.properties["version"] == "2.0"
    
    @pytest.mark.dependency(depends=["TestComponentRepository::test_update_component"])
    def test_delete_component(self):
        """Test deleting a component."""
        repo = ComponentRepository()
        
        # Delete the component
        global component_id
        result = repo.delete(component_id)
        assert result is True
        
        # Verify it was deleted
        fetched = repo.get_by_id(component_id)
        assert fetched is None


class TestSystemRepository:
    """Tests for the SystemRepository."""
    
    @pytest.fixture
    def setup_components(self):
        """Create test components for system tests."""
        repo = ComponentRepository()
        comp1 = Component(name="System Test Component 1", type="software")
        comp2 = Component(name="System Test Component 2", type="hardware")
        comp1 = repo.upsert(comp1)
        comp2 = repo.upsert(comp2)
        
        global system_components
        system_components = [comp1, comp2]
        return [comp1, comp2]
    
    @pytest.mark.dependency()
    def test_create_system(self, setup_components):
        """Test creating a system."""
        repo = SystemRepository()
        
        # Get components from fixture
        components = setup_components
        
        system = System(
            name="Test System",
            components=[components[0].uuid, components[1].uuid],
            properties={"environment": "development"},
        )
        
        # Create the system
        result = repo.upsert(system)
        assert result.name == "Test System"
        
        # Save the system UUID for next tests
        global system_id
        system_id = result.uuid
        
        # Verify it was created
        fetched = repo.get_by_id(result.uuid)
        assert fetched is not None
        assert fetched.name == "Test System"
        assert len(fetched.components) == 2
        
        # Check components were associated
        component_uuids = [str(c) for c in fetched.components]
        comp_ids = [str(c.uuid) for c in components]
        for c_id in comp_ids:
            assert c_id in component_uuids
    
    @pytest.mark.dependency(depends=["TestSystemRepository::test_create_system"])
    def test_update_system(self):
        """Test updating a system."""
        repo = SystemRepository()
        
        # Get the system
        global system_id, system_components
        system = repo.get_by_id(system_id)
        assert system is not None
        
        # Update the system
        system.name = "Updated System"
        system.properties["status"] = "active"
        
        # Remove one component to test updates to component list
        system.components = [system.components[0]]
        result = repo.upsert(system)
        
        # Verify the update
        assert result.name == "Updated System"
        assert result.properties["status"] == "active"
        assert len(result.components) == 1
        
        # Check that it was persisted
        fetched = repo.get_by_id(system_id)
        assert fetched is not None
        assert fetched.name == "Updated System"
        assert fetched.properties["status"] == "active"
        assert len(fetched.components) == 1
        assert str(fetched.components[0]) == str(system_components[0].uuid)
    
    @pytest.mark.dependency(depends=["TestSystemRepository::test_update_system"])
    def test_delete_system(self):
        """Test deleting a system."""
        repo = SystemRepository()
        
        # Delete the system
        global system_id
        result = repo.delete(system_id)
        assert result is True
        
        # Verify it was deleted
        fetched = repo.get_by_id(system_id)
        assert fetched is None
