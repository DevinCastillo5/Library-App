# crud/publishers_crud.py
from typing import List
from fastapi import HTTPException
from databases import Database
from schemas.publishers import Publishers
from database import database  # your database.py file

TABLE_NAME = "Publishers"

# Ensure connection is active
async def ensure_connection():
    if not database.is_connected:
        await database.connect()

# Get all publishers with optional pagination
async def get_publishers(skip: int = 0, limit: int = 100) -> List[Publishers]:
    await ensure_connection()
    query = f"SELECT PublishName, ContactInfo FROM {TABLE_NAME} LIMIT :limit OFFSET :skip"
    rows = await database.fetch_all(query=query, values={"skip": skip, "limit": limit})
    return [Publishers(**row) for row in rows]

# Get a single publisher by name
async def get_publisher(name: str) -> Publishers:
    await ensure_connection()
    query = f"SELECT PublishName, ContactInfo FROM {TABLE_NAME} WHERE PublishName = :name"
    row = await database.fetch_one(query=query, values={"name": name})
    if row:
        return Publishers(**row)
    raise HTTPException(status_code=404, detail="Publisher not found")

# Create a new publisher
async def create_publisher(publisher: Publishers) -> Publishers:
    await ensure_connection()
    query = f"""
        INSERT INTO {TABLE_NAME} (PublishName, ContactInfo)
        VALUES (:PublishName, :ContactInfo)
    """
    await database.execute(query=query, values=publisher.dict())
    return publisher

# Update an existing publisher
async def update_publisher(publisher: Publishers) -> Publishers:
    await ensure_connection()
    query = f"""
        UPDATE {TABLE_NAME}
        SET ContactInfo = :ContactInfo
        WHERE PublishName = :PublishName
    """
    await database.execute(query=query, values=publisher.dict())
    return publisher

# Delete a publisher by name
async def delete_publisher(name: str):
    await ensure_connection()
    query = f"DELETE FROM {TABLE_NAME} WHERE PublishName = :name"
    await database.execute(query=query, values={"name": name})

# Delete multiple publishers by names
async def delete_publishers(PublishNames: List[str]) -> int:
    if not PublishNames:
        return 0  # Nothing to delete
    await ensure_connection()
    query = f"DELETE FROM {TABLE_NAME} WHERE PublishName IN :PublishNames"
    return await database.execute(query=query, values={"PublishNames": PublishNames})
