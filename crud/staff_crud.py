# crud/staff_crud.py
from typing import List
from fastapi import HTTPException
from schemas.staff import Staff
from database import database  # your database.py file

TABLE_NAME = "Staff"

# Ensure connection is active
async def ensure_connection():
    if not database.is_connected:
        await database.connect()


# Get all staff members (optional pagination)
async def get_staff(skip: int = 0, limit: int = 100) -> List[Staff]:
    await ensure_connection()
    query = f"""
        SELECT StaffID, StaffName, Position, WorkTime
        FROM {TABLE_NAME}
        LIMIT :limit OFFSET :skip
    """
    rows = await database.fetch_all(query=query, values={"skip": skip, "limit": limit})
    return [Staff(**row) for row in rows]


# Get one staff member
async def get_staff_member(staff_id: int) -> Staff:
    await ensure_connection()
    query = f"""
        SELECT StaffID, StaffName, Position, WorkTime
        FROM {TABLE_NAME}
        WHERE StaffID = :staff_id
    """
    row = await database.fetch_one(query=query, values={"staff_id": staff_id})
    if row:
        return Staff(**row)
    raise HTTPException(status_code=404, detail="Staff member not found")


# Create new staff member
async def create_staff(staff: Staff) -> Staff:
    await ensure_connection()
    query = f"""
        INSERT INTO {TABLE_NAME} (StaffID, StaffName, Position, WorkTime)
        VALUES (:StaffID, :StaffName, :Position, :WorkTime)
    """
    await database.execute(query=query, values=staff.dict())
    return staff


# Update staff
async def update_staff(staff: Staff) -> Staff:
    await ensure_connection()
    query = f"""
        UPDATE {TABLE_NAME}
        SET StaffName = :StaffName,
            Position = :Position,
            WorkTime = :WorkTime
        WHERE StaffID = :StaffID
    """
    await database.execute(query=query, values=staff.dict())
    return staff


# Delete staff
async def delete_staff(staff_id: int):
    await ensure_connection()
    query = f"DELETE FROM {TABLE_NAME} WHERE StaffID = :staff_id"
    await database.execute(query=query, values={"staff_id": staff_id})
