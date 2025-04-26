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

from typing import List, Optional
from uuid import UUID

from .models import Component, System
from .repositories import ComponentRepository, SystemRepository


class ComponentService:
    """Service for managing components."""

    def __init__(self):
        self.repository = ComponentRepository()

    def create_or_update(self, component: Component) -> Component:
        """Create or update a component."""
        return self.repository.upsert(component)

    def get(self, uuid: UUID) -> Optional[Component]:
        """Get a component by UUID."""
        return self.repository.get_by_id(uuid)

    def get_all(self) -> List[Component]:
        """Get all components."""
        return self.repository.get_all()

    def delete(self, uuid: UUID) -> bool:
        """Delete a component."""
        return self.repository.delete(uuid)

    def get_by_type(self, component_type: str) -> List[Component]:
        """Get components by type."""
        all_components = self.repository.get_all()
        return [c for c in all_components if c.type == component_type]


class SystemService:
    """Service for managing systems."""
    
    def __init__(self):
        self.repository = SystemRepository()
        self.component_repository = ComponentRepository()

    def create_or_update(self, system: System) -> System:
        """Create or update a system."""
        return self.repository.upsert(system)

    def get(self, uuid: UUID) -> Optional[System]:
        """Get a system by UUID."""
        return self.repository.get_by_id(uuid)

    def get_all(self) -> List[System]:
        """Get all systems."""
        return self.repository.get_all()

    def delete(self, uuid: UUID) -> bool:
        """Delete a system."""
        return self.repository.delete(uuid)

    def get_full_system(self, uuid: UUID) -> Optional[System]:
        """Get a system with all component details."""
        system = self.repository.get_by_id(uuid)
        if not system:
            return None
        
        # Replace component UUIDs with actual component objects
        loaded_components = []
        for comp_uuid in system.components:
            component = self.component_repository.get_by_id(comp_uuid)
            if component:
                loaded_components.append(component)
        
        # Create a new system object with loaded components
        full_system = System(
            uuid=system.uuid,
            name=system.name,
            components=loaded_components,
            properties=system.properties
        )
        
        return full_system

    def add_component_to_system(
        self, system_uuid: UUID, component_uuid: UUID
    ) -> Optional[System]:
        """Add a component to a system."""
        system = self.repository.get_by_id(system_uuid)
        if not system:
            return None

        component = self.component_repository.get_by_id(component_uuid)
        if not component:
            return None

        # Add component UUID if not already in the system
        if component_uuid not in system.components:
            system.components.append(component_uuid)
            self.repository.upsert(system)

        return system

    def remove_component_from_system(
        self, system_uuid: UUID, component_uuid: UUID
    ) -> Optional[System]:
        """Remove a component from a system."""
        system = self.repository.get_by_id(system_uuid)
        if not system:
            return None

        # Remove component UUID if it exists in the system
        if component_uuid in system.components:
            system.components.remove(component_uuid)
            self.repository.upsert(system)

        return system
