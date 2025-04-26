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
from pydantic import ValidationError

from archman.models import Component, System


class TestComponentModel:
    """Test cases for Component model."""

    def test_valid_component_creation(self):
        """Test creating a valid component."""
        component = Component(
            name="Test Component",
            type="software",
            properties={"language": "Python"},
        )
        assert component.name == "Test Component"
        assert component.type == "software"
        assert component.properties == {"language": "Python"}
        assert isinstance(component.uuid, UUID)

    def test_component_invalid_type(self):
        """Test component creation with invalid type."""
        with pytest.raises(ValidationError):
            Component(
                name="Test Component",
                type="invalid_type",  # Not one of the allowed types
                properties={},
            )

    def test_component_dict_for_db(self):
        """Test component's dict_for_db method."""
        component = Component(
            name="Database",
            type="database",
            properties={"vendor": "PostgreSQL"},
        )
        db_dict = component.dict_for_db()
        
        assert isinstance(db_dict, dict)
        assert db_dict["name"] == "Database"
        assert db_dict["type"] == "database"
        assert db_dict["properties"] == {"vendor": "PostgreSQL"}
        assert isinstance(db_dict["uuid"], str)


class TestSystemModel:
    """Test cases for System model."""

    def test_valid_system_creation(self):
        """Test creating a valid system."""
        system = System(
            name="Test System",
            properties={"environment": "production"},
        )
        assert system.name == "Test System"
        assert system.properties == {"environment": "production"}
        assert system.components == []
        assert isinstance(system.uuid, UUID)

    def test_system_with_components(self):
        """Test creating a system with components."""
        component1 = Component(name="Component 1", type="software")
        component2 = Component(name="Component 2", type="hardware")
        
        system = System(
            name="Test System",
            components=[component1, component2],
        )
        
        assert len(system.components) == 2
        assert component1 in system.components
        assert component2 in system.components

    def test_system_dict_for_db(self):
        """Test system's dict_for_db method."""
        component1 = Component(name="Component 1", type="software")
        component2 = Component(name="Component 2", type="hardware")
        
        system = System(
            name="System with Components",
            components=[component1, component2],
            properties={"status": "active"},
        )
        
        db_dict = system.dict_for_db()
        
        assert isinstance(db_dict, dict)
        assert db_dict["name"] == "System with Components"
        assert db_dict["properties"] == {"status": "active"}
        assert len(db_dict["components"]) == 2
        assert isinstance(db_dict["components"][0], str)
        assert isinstance(db_dict["components"][1], str)
        assert isinstance(db_dict["uuid"], str)
