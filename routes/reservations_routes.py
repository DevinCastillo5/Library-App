from fastapi import APIRouter, HTTPException
from typing import List
from database import database
from schemas.reservations import Reservations
from crud.reservations_crud import (
    get_reservations, get_reservation, create_reservation,
    update_reservation, delete_reservation, get_reservations_by_member
)

router = APIRouter(prefix="/api/reservations", tags=["Reservations"])

# GET all reservations
@router.get("/", response_model=List[Reservations])
async def api_get_reservations(skip: int = 0, limit: int = 10):
    async with database:
        rows = await get_reservations(skip, limit)
        return [Reservations(**dict(r)) for r in rows]
    
# GET one reservation by reservationID
@router.get("/{reservationID}", response_model=Reservations)
async def api_get_reservation(reservationID: int):
    async with database:
        reservation = await get_reservation(reservationID)
        if not reservation:
            raise HTTPException(status_code=404, detail="Reservation not found")
        return Reservations(**reservation)
    
# POST: Create new reservation
@router.post("/", response_model=Reservations)
async def api_create_reservation(reservation: Reservations):
    async with database:
        new_reservation = await create_reservation(reservation)
        return Reservations(**new_reservation)
    
# PUT: Update existing reservation
@router.put("/", response_model=Reservations)
async def api_update_reservation(reservation: Reservations):
    async with database:
        try:
            await update_reservation(reservation.ReservationID, reservation.DateFor, reservation.memberID, reservation.BookReserved)
            return reservation
        except ValueError as err:
            raise HTTPException(status_code=400, detail=str(err))

# DELETE: Delete a single reservation
@router.delete("/{reservationID}")
async def api_delete_reservation(reservationID: int):
    async with database:
        deleted = await delete_reservation(reservationID)
        if not deleted:
            raise HTTPException(status_code=404, detail="Reservation not found")
        return {"detail": f"Reservation '{reservationID}' deleted"}

# GET reservations by memberID
@router.get("/member/{memberID}", response_model=List[Reservations])
async def api_get_reservations_by_member(memberID: int):
    async with database:
        rows = await get_reservations_by_member(memberID)
        return [Reservations(**dict(r)) for r in rows]
