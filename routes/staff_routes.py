# routes/staff_routes.py
from fastapi import APIRouter
from schemas.staff import Staff
import crud.staff_crud as crud

router = APIRouter(prefix="/staff", tags=["Staff"])


@router.get("/")
async def get_staff(skip: int = 0, limit: int = 100):
    return await crud.get_staff(skip, limit)


@router.get("/{staff_id}")
async def get_staff_member(staff_id: int):
    return await crud.get_staff_member(staff_id)


@router.post("/")
async def create_staff(staff: Staff):
    return await crud.create_staff(staff)


@router.put("/")
async def update_staff(staff: Staff):
    return await crud.update_staff(staff)


@router.delete("/{staff_id}")
async def delete_staff(staff_id: int):
    return await crud.delete_staff(staff_id)