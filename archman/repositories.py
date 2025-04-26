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

import json
from typing import List, Optional
from uuid import UUID

from .models import Component, System
from .db import get_connection


class ComponentRepository:
    """Repository for Component entities."""
    
    def upsert(self, component: Component) -> Component:
        """Create or update a component."""
        conn = get_connection()
        data = component.dict_for_db()
        
        # Convert properties to JSON string
        properties_json = json.dumps(data['properties'])
        
        # Check if component exists
        exists = conn.execute(
            "SELECT 1 FROM components WHERE uuid = ?", 
            (data['uuid'],)
        ).fetchone()
        
        if exists:
            # Update existing component
            conn.execute("""
                UPDATE components 
                SET name = ?, type = ?, properties = ?
                WHERE uuid = ?
            """, (data['name'], data['type'], properties_json, data['uuid']))
        else:
            # Insert new component
            conn.execute("""
                INSERT INTO components (uuid, name, type, properties)
                VALUES (?, ?, ?, ?)
            """, (data['uuid'], data['name'], data['type'], properties_json))
        
        return component

    def get_by_id(self, uuid: UUID) -> Optional[Component]:
        """Get a component by UUID."""
        conn = get_connection()
        result = conn.execute(
            """
            SELECT uuid, name, type, properties
            FROM components
            WHERE uuid = ?
        """,
            (str(uuid),),
        ).fetchone()

        if not result:
            return None

        uuid_str, name, type_str, properties_json = result
        properties = json.loads(properties_json) if properties_json else {}

        return Component(
            uuid=UUID(uuid_str), name=name, type=type_str, properties=properties
        )

    def get_all(self) -> List[Component]:
        """Get all components."""
        conn = get_connection()
        results = conn.execute(
            """
            SELECT uuid, name, type, properties
            FROM components
        """
        ).fetchall()

        components = []
        for uuid_str, name, type_str, properties_json in results:
            properties = json.loads(properties_json) if properties_json else {}
            components.append(
                Component(
                    uuid=UUID(uuid_str), name=name, type=type_str, properties=properties
                )
            )

        return components

    def delete(self, uuid: UUID) -> bool:
        """Delete a component by UUID."""
        conn = get_connection()
        conn.execute("DELETE FROM components WHERE uuid = ?", (str(uuid),))
        return True


class SystemRepository:
    """Repository for System entities."""
    
    def upsert(self, system: System) -> System:
        """Create or update a system."""
        conn = get_connection()
        data = system.dict_for_db()
        
        # Convert collections to JSON strings
        components_json = json.dumps(data['components'])
        properties_json = json.dumps(data['properties'])
        
        # Check if system exists
        exists = conn.execute(
            "SELECT 1 FROM systems WHERE uuid = ?", 
            (data['uuid'],)
        ).fetchone()
        
        if exists:
            # Update existing system
            conn.execute("""
                UPDATE systems 
                SET name = ?, components = ?, properties = ?
                WHERE uuid = ?
            """, (data['name'], components_json, properties_json, data['uuid']))
        else:
            # Insert new system
            conn.execute("""
                INSERT INTO systems (uuid, name, components, properties)
                VALUES (?, ?, ?, ?)
            """, (data['uuid'], data['name'], components_json, properties_json))
        
        return system

    def get_by_id(self, uuid: UUID) -> Optional[System]:
        """Get a system by UUID."""
        conn = get_connection()
        result = conn.execute(
            """
            SELECT uuid, name, components, properties
            FROM systems
            WHERE uuid = ?
        """,
            (str(uuid),),
        ).fetchone()

        if not result:
            return None

        uuid_str, name, components_json, properties_json = result
        components = (
            [UUID(comp_id) for comp_id in json.loads(components_json)]
            if components_json
            else []
        )
        properties = json.loads(properties_json) if properties_json else {}

        return System(
            uuid=UUID(uuid_str), name=name, components=components, properties=properties
        )

    def get_all(self) -> List[System]:
        """Get all systems."""
        conn = get_connection()
        results = conn.execute(
            """
            SELECT uuid, name, components, properties
            FROM systems
        """
        ).fetchall()

        systems = []
        for uuid_str, name, components_json, properties_json in results:
            components = (
                [UUID(comp_id) for comp_id in json.loads(components_json)]
                if components_json
                else []
            )
            properties = json.loads(properties_json) if properties_json else {}
            systems.append(
                System(
                    uuid=UUID(uuid_str),
                    name=name,
                    components=components,
                    properties=properties,
                )
            )

        return systems

    def delete(self, uuid: UUID) -> bool:
        """Delete a system by UUID."""
        conn = get_connection()
        conn.execute("DELETE FROM systems WHERE uuid = ?", (str(uuid),))
        return True
