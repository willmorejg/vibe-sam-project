from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime

router = APIRouter(
    prefix="/components",
    tags=["components"],
    responses={404: {"description": "Not found"}},
)

# In-memory storage for components (replace with database in production)
components_db = {}

class ComponentBase(BaseModel):
    name: str
    description: Optional[str] = None
    system_id: Optional[str] = None
    properties: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None

class ComponentCreate(ComponentBase):
    pass

class Component(ComponentBase):
    id: str
    created_at: datetime
    updated_at: datetime

@router.post("/", response_model=Component, status_code=status.HTTP_201_CREATED)
async def create_component(component: ComponentCreate):
    """Create a new component"""
    component_id = str(uuid.uuid4())
    current_time = datetime.now()
    
    component_data = Component(
        id=component_id,
        created_at=current_time,
        updated_at=current_time,
        **component.model_dump()
    )
    
    components_db[component_id] = component_data
    return component_data

@router.put("/{component_id}", response_model=Component)
async def update_component(component_id: str, component: ComponentCreate):
    """Update an existing component"""
    if component_id not in components_db:
        raise HTTPException(status_code=404, detail="Component not found")
    
    stored_component = components_db[component_id]
    current_time = datetime.now()
    
    update_data = component.model_dump(exclude_unset=True)
    
    for key, value in update_data.items():
        setattr(stored_component, key, value)
    
    stored_component.updated_at = current_time
    components_db[component_id] = stored_component
    
    return stored_component

@router.get("/{component_id}", response_model=Component)
async def read_component(component_id: str):
    """Get a component by ID"""
    if component_id not in components_db:
        raise HTTPException(status_code=404, detail="Component not found")
    
    return components_db[component_id]

@router.get("/", response_model=List[Component])
async def read_all_components():
    """Get all components"""
    return list(components_db.values())

@router.delete("/{component_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_component(component_id: str):
    """Delete a component by ID"""
    if component_id not in components_db:
        raise HTTPException(status_code=404, detail="Component not found")
    
    del components_db[component_id]
    return None
