# crud/reservations_crud.py
from typing import List
from fastapi import HTTPException
from databases import Database
from schemas.reservations import Reservations, ReservationCreate, ReservationRequest
from datetime import date
from database import database  # your database.py file

TABLE_NAME = "Reservations"

# Ensure connection is active
async def ensure_connection():
    if not database.is_connected:
        await database.connect()

async def get_reservations(skip: int = 0, limit: int = 100) -> List[Reservations]:
    await ensure_connection()
    query = f"""
        SELECT ReservationID, ISBN, MemberID, CopyID, ReserveDate
        FROM {TABLE_NAME}
        LIMIT :limit OFFSET :skip
    """
    rows = await database.fetch_all(query=query, values={"skip": skip, "limit": limit})
    return [Reservations(**dict(row)) for row in rows]


# Get a single reservation by ID
async def get_reservation(reservation_id: int) -> Reservations:
    await ensure_connection()
    query = f"""
        SELECT ReservationID, ISBN, MemberID, CopyID, ReserveDate
        FROM {TABLE_NAME}
        WHERE ReservationID = :reservation_id
    """
    row = await database.fetch_one(query=query, values={"reservation_id": reservation_id})
    if row:
        return Reservations(**dict(row))
    raise HTTPException(status_code=404, detail="Reservation not found")

async def create_reservation(reservation: ReservationCreate) -> Reservations:
    await ensure_connection()
    query = """
        INSERT INTO Reservations (ISBN, MemberID, CopyID, ReserveDate)
        VALUES (:ISBN, :MemberID, :CopyID, :ReserveDate)
    """
    values = reservation.dict()
    await database.execute(query=query, values=values)

    row = await database.fetch_one(
        "SELECT ReservationID, ISBN, MemberID, CopyID, ReserveDate FROM Reservations ORDER BY ReservationID DESC LIMIT 1"
    )
    return Reservations(**dict(row))




async def update_reservation(reservation: Reservations) -> Reservations:
    await ensure_connection()
    query = f"""
        UPDATE {TABLE_NAME}
        SET ISBN = :ISBN,
            MemberID = :MemberID,
            CopyID = :CopyID,
            ReserveDate = :ReserveDate
        WHERE ReservationID = :ReservationID
    """
    values = reservation.dict()
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