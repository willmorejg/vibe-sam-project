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

from typing import Dict, List, Literal, Any, Union
from pydantic import BaseModel, Field
from uuid import uuid4, UUID

ComponentType = Literal["hardware", "software", "database", "people", "process"]

class Component(BaseModel):
    """Component represents an individual part of the architecture."""
    uuid: UUID = Field(default_factory=uuid4)
    name: str
    type: ComponentType
    properties: Dict[str, Any] = Field(default_factory=dict)
    
    def dict_for_db(self) -> Dict[str, Any]:
        """Convert to a dict format suitable for DB storage."""
        return {
            "uuid": str(self.uuid),
            "name": self.name,
            "type": self.type,
            "properties": self.properties
        }

class System(BaseModel):
    """System is a collection of one or more components."""
    uuid: UUID = Field(default_factory=uuid4)
    name: str
    components: List[Union[UUID, Component]] = Field(default_factory=list)
    properties: Dict[str, Any] = Field(default_factory=dict)
    
    def dict_for_db(self) -> Dict[str, Any]:
        """Convert to a dict format suitable for DB storage."""
        # Convert component objects to UUIDs if needed
        component_uuids = []
        for comp in self.components:
            if isinstance(comp, Component):
                component_uuids.append(str(comp.uuid))
            else:
                component_uuids.append(str(comp))
                
        return {
            "uuid": str(self.uuid),
            "name": self.name,
            "components": component_uuids,
            "properties": self.properties
        }
