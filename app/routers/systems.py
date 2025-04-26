from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime

router = APIRouter(
    prefix="/systems",
    tags=["systems"],
    responses={404: {"description": "Not found"}},
)

# In-memory storage for systems (replace with database in production)
systems_db = {}

class SystemBase(BaseModel):
    name: str
    description: Optional[str] = None
    properties: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None

class SystemCreate(SystemBase):
    pass

class System(SystemBase):
    id: str
    created_at: datetime
    updated_at: datetime

@router.post("/", response_model=System, status_code=status.HTTP_201_CREATED)
async def create_or_update_system(system: SystemCreate):
    """Create a new system or update if ID is provided in request body"""
    system_id = str(uuid.uuid4())
    current_time = datetime.now()
    
    system_data = System(
        id=system_id,
        created_at=current_time,
        updated_at=current_time,
        **system.model_dump()
    )
    
    systems_db[system_id] = system_data
    return system_data

@router.put("/{system_id}", response_model=System)
async def update_system(system_id: str, system: SystemCreate):
    """Update an existing system"""
    if system_id not in systems_db:
        raise HTTPException(status_code=404, detail="System not found")
    
    stored_system = systems_db[system_id]
    current_time = datetime.now()
    
    update_data = system.model_dump(exclude_unset=True)
    
    for key, value in update_data.items():
        setattr(stored_system, key, value)
    
    stored_system.updated_at = current_time
    systems_db[system_id] = stored_system
    
    return stored_system

@router.get("/{system_id}", response_model=System)
async def read_system(system_id: str):
    """Get a system by ID"""
    if system_id not in systems_db:
        raise HTTPException(status_code=404, detail="System not found")
    
    return systems_db[system_id]

@router.get("/", response_model=List[System])
async def read_all_systems():
    """Get all systems"""
    return list(systems_db.values())

@router.delete("/{system_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_system(system_id: str):
    """Delete a system by ID"""
    if system_id not in systems_db:
        raise HTTPException(status_code=404, detail="System not found")
    
    del systems_db[system_id]
    return None
