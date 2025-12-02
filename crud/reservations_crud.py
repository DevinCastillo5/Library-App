# crud/reservations_crud.py
from typing import List
from fastapi import HTTPException
from databases import Database
from schemas.reservations import Reservations
from database import database  # your database.py file

TABLE_NAME = "Reservations"

# Ensure connection is active
async def ensure_connection():
    if not database.is_connected:
        await database.connect()

# Get all reservations with optional pagination
async def get_reservations(skip: int = 0, limit: int = 100) -> List[Reservations]:
    await ensure_connection()
    query = f"SELECT ReservationID, memberID, DateFor, BookReserved FROM {TABLE_NAME} LIMIT :limit OFFSET :skip"
    rows = await database.fetch_all(query=query, values={"skip": skip, "limit": limit})
    # Convert DateFor to date object
    return [Reservations(**{**row, "DateFor": row["DateFor"]}) for row in rows]

# Get a single reservation by ID
async def get_reservation(reservation_id: int) -> Reservations:
    await ensure_connection()
    query = f"SELECT ReservationID, memberID, DateFor, BookReserved FROM {TABLE_NAME} WHERE ReservationID = :reservation_id"
    row = await database.fetch_one(query=query, values={"reservation_id": reservation_id})
    if row:
        return Reservations(**{**row, "DateFor": row["DateFor"]})
    raise HTTPException(status_code=404, detail="Reservation not found")

# Create a new reservation
async def create_reservation(reservation: Reservations) -> Reservations:
    await ensure_connection()
    query = f"""
        INSERT INTO {TABLE_NAME} (ReservationID, memberID, DateFor, BookReserved)
        VALUES (:ReservationID, :memberID, :DateFor, :BookReserved)
    """
    # Convert DateFor to string for SQL
    values = {**reservation.dict(), "DateFor": reservation.DateFor.isoformat()}
    await database.execute(query=query, values=values)
    return reservation

# Update an existing reservation
async def update_reservation(reservation: Reservations) -> Reservations:
    await ensure_connection()
    query = f"""
        UPDATE {TABLE_NAME}
        SET memberID = :memberID,
            DateFor = :DateFor,
            BookReserved = :BookReserved
        WHERE ReservationID = :ReservationID
    """
    values = {**reservation.dict(), "DateFor": reservation.DateFor.isoformat()}
    await database.execute(query=query, values=values)
    return reservation

# Delete a reservation by ID
async def delete_reservation(reservation_id: int):
    await ensure_connection()
    query = f"DELETE FROM {TABLE_NAME} WHERE ReservationID = :reservation_id"
    await database.execute(query=query, values={"reservation_id": reservation_id})

# delete reservations by memberID
async def delete_reservations_by_member(member_id: int):
    await ensure_connection()
    query = f"DELETE FROM {TABLE_NAME} WHERE memberID = :member_id"
    await database.execute(query=query, values={"member_id": member_id})