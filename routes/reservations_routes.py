# routes/reservations_routes.py
from fastapi import APIRouter, HTTPException
from typing import List
from schemas.reservations import Reservations, ReservationCreate, ReservationRequest
from datetime import date
from database import database
from crud.reservations_crud import (
    get_reservations,
    get_reservation,
    create_reservation,
    update_reservation,
    delete_reservation,
    delete_reservations_by_member,
)

router = APIRouter(prefix="/api/reservations", tags=["Reservations"])

@router.get("/", response_model=List[Reservations])
async def api_get_reservations(skip: int = 0, limit: int = 100):
    return await get_reservations(skip, limit)

@router.get("/{reservation_id}", response_model=Reservations)
async def api_get_reservation(reservation_id: int):
    return await get_reservation(reservation_id)

@router.post("/", response_model=Reservations)
async def api_create_reservation(req: ReservationRequest):
    query = """
        SELECT c.CopyID
        FROM Copies c
        INNER JOIN Loans l ON c.CopyID = l.CopyID
        WHERE c.ISBN = :isbn AND l.ReturnDate IS NULL
        LIMIT 1
    """
    row = await database.fetch_one(query=query, values={"isbn": req.ISBN})
    if not row:
        raise HTTPException(status_code=404, detail="No loaned copy available to reserve")

    copy_id = row["CopyID"]

    reservation = ReservationCreate(
        ISBN=req.ISBN,
        MemberID=req.MemberID,
        CopyID=copy_id,
        ReserveDate=date.today(),
    )

    return await create_reservation(reservation)



@router.put("/", response_model=Reservations)
async def api_update_reservation(reservation: Reservations):
    return await update_reservation(reservation)

@router.delete("/{reservation_id}")
async def api_delete_reservation(reservation_id: int):
    await delete_reservation(reservation_id)
    return {"detail": "Reservation deleted"}

@router.delete("/member/{member_id}")
async def api_delete_reservations_by_member(member_id: int):
    await delete_reservations_by_member(member_id)
    return {"detail": "Reservations for member deleted"}