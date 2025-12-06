from fastapi import APIRouter, HTTPException
from typing import List
from schemas.publishers import Publishers
from crud.publishers_crud import (
    get_publishers,
    get_publisher,
    create_publisher,
    update_publisher,
    delete_publisher,
    delete_publishers
)
from database import database  # database instance

router = APIRouter(prefix="/api/publishers", tags=["Publishers"])

# Ensure database connection
@router.on_event("startup")
async def startup():
    if not database.is_connected:
        await database.connect()

@router.on_event("shutdown")
async def shutdown():
    if database.is_connected:
        await database.disconnect()

# Get all publishers
@router.get("/", response_model=List[Publishers])
async def api_get_publishers(skip: int = 0, limit: int = 100):
    return await get_publishers(skip, limit)

# Get publisher by name
@router.get("/{name}", response_model=Publishers)
async def api_get_publisher(name: str):
    publisher = await get_publisher(name)
    if not publisher:
        raise HTTPException(status_code=404, detail="Publisher not found")
    return publisher

# Create publisher
@router.post("/", response_model=Publishers)
async def api_create_publisher(publisher: Publishers):
    return await create_publisher(publisher)

# Update publisher
@router.put("/", response_model=Publishers)
async def api_update_publisher(publisher: Publishers):
    return await update_publisher(publisher)

# Delete publisher
@router.delete("/{name}")
async def api_delete_publisher(name: str):
    await delete_publisher(name)
    return {"detail": "Publisher deleted"}

# Delete multiple publishers
@router.delete("/")
async def api_delete_publishers(PublishNames: List[str]):
    deleted_count = await delete_publishers(PublishNames)
    return {"detail": f"Deleted {deleted_count} publishers"}