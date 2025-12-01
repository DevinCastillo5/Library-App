from fastapi import APIRouter, HTTPException
from typing import List
from database import database
from schemas.staff import Staff
from crud.staff_crud import (
    get_staff, get_staff_member, create_staff, update_staff, delete_staff
)

router = APIRouter(prefix="/api/staff", tags=["Staff"])

# GET all staff members
@router.get("/", response_model=List[Staff])
async def api_get_staff(skip: int = 0, limit: int = 10):
    async with database:
        rows = await get_staff(skip, limit)
        return [Staff(**dict(r)) for r in rows]
    
# GET one staff member by StaffID
@router.get("/{StaffID}", response_model=Staff)
async def api_get_staff_member(StaffID: int):
    async with database:
        staff_member = await get_staff_member(StaffID)
        if not staff_member:
            raise HTTPException(status_code=404, detail="Staff member not found")
        return Staff(**staff_member)
    
# POST: Create new staff member
@router.post("/", response_model=Staff)
async def api_create_staff(staff: Staff):
    async with database:
        new_staff_id = await create_staff(staff.StaffID, staff.StaffName, staff.Position, staff.WorkTime)
        return Staff(**staff.dict())

# PUT: Update existing staff member
@router.put("/", response_model=Staff)
async def api_update_staff(staff: Staff):
    async with database:
        try:
            await update_staff(staff.StaffID, staff.StaffName, staff.Position, staff.WorkTime)
            return staff
        except ValueError as err:
            raise HTTPException(status_code=400, detail=str(err))

# DELETE: Delete a single staff member
@router.delete("/{StaffID}")
async def api_delete_staff(StaffID: int):
    async with database:
        deleted = await delete_staff(StaffID)
        if not deleted:
            raise HTTPException(status_code=404, detail="Staff member not found")
        return {"detail": f"Staff member '{StaffID}' deleted"}