# routes/reservations_routes.py
from fastapi import APIRouter, HTTPException
from typing import List
from schemas.reservations import Reservations
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
async def api_create_reservation(reservation: Reservations):
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