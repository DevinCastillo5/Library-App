from typing import List, Optional
from fastapi import HTTPException
from schemas.members import Members
from database import database  # Your Database instance

TABLE_NAME = "Members"

# Ensure database connection
async def ensure_connection():
    if not database.is_connected:
        await database.connect()


# Fetch all members with optional pagination
async def get_members(skip: int = 0, limit: int = 100) -> List[Members]:
    await ensure_connection()
    query = f"""
        SELECT memberID, memName, Email, Phone, Address
        FROM {TABLE_NAME}
        LIMIT :limit OFFSET :skip
    """
    rows = await database.fetch_all(query=query, values={"skip": skip, "limit": limit})
    return [Members(**dict(row)) for row in rows]


# Fetch a single member by memberID
async def get_member(memberID: int) -> Members:
    await ensure_connection()
    query = f"""
        SELECT memberID, memName, Email, Phone, Address
        FROM {TABLE_NAME}
        WHERE memberID = :memberID
    """
    row = await database.fetch_one(query=query, values={"memberID": memberID})
    if row:
        return Members(**dict(row))
    raise HTTPException(status_code=404, detail="Member not found")


# Create a new member
async def create_member(member: Members) -> Members:
    await ensure_connection()
    query = f"""
        INSERT INTO {TABLE_NAME} (memberID, memName, Email, Phone, Address)
        VALUES (:memberID, :memName, :Email, :Phone, :Address)
    """
    await database.execute(query=query, values=member.dict())
    return member


# Update an existing member
async def update_member(member: Members) -> Members:
    await ensure_connection()
    query = f"""
        UPDATE {TABLE_NAME}
        SET memName = :memName,
            Email = :Email,
            Phone = :Phone,
            Address = :Address
        WHERE memberID = :memberID
    """
    await database.execute(query=query, values=member.dict())
    return member


# Delete a member by memberID
async def delete_member(memberID: int) -> None:
    await ensure_connection()
    query = f"DELETE FROM {TABLE_NAME} WHERE memberID = :memberID"
    await database.execute(query=query, values={"memberID": memberID})
