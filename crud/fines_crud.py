# crud/fines_crud.py
from typing import List
from databases import Database
from fastapi import HTTPException
from schemas.fines import Fines
from database import database  # your database.py file

TABLE_NAME = "Fines"

# Ensure connection is active
async def ensure_connection():
    if not database.is_connected:
        await database.connect()


# Get all fines with optional pagination
async def get_fines(skip: int = 0, limit: int = 100) -> List[Fines]:
    await ensure_connection()
    query = f"SELECT * FROM {TABLE_NAME} LIMIT :limit OFFSET :skip"
    rows = await database.fetch_all(query=query, values={"skip": skip, "limit": limit})
    return [Fines(**row) for row in rows]


# Get a single fine by FineID
async def get_fine(fine_id: int) -> Fines:
    await ensure_connection()
    query = f"SELECT * FROM {TABLE_NAME} WHERE FineID = :fine_id"
    row = await database.fetch_one(query=query, values={"fine_id": fine_id})
    if row:
        return Fines(**row)
    raise HTTPException(status_code=404, detail="Fine not found")


# Create a new fine
async def create_fine(fine: Fines) -> Fines:
    await ensure_connection()
    query = f"""
    INSERT INTO {TABLE_NAME} (FineID, AmountFined, DaysOverdue, LoanID)
    VALUES (:FineID, :AmountFined, :DaysOverdue, :LoanID)
    """
    await database.execute(query=query, values=fine.dict())
    return fine


# Update an existing fine
async def update_fine(fine: Fines) -> Fines:
    await ensure_connection()
    query = f"""
    UPDATE {TABLE_NAME}
    SET AmountFined = :AmountFined,
        DaysOverdue = :DaysOverdue,
        LoanID = :LoanID
    WHERE FineID = :FineID
    """
    result = await database.execute(query=query, values=fine.dict())
    return fine


# Delete a fine by FineID
async def delete_fine(fine_id: int):
    await ensure_connection()
    query = f"DELETE FROM {TABLE_NAME} WHERE FineID = :fine_id"
    await database.execute(query=query, values={"fine_id": fine_id})
