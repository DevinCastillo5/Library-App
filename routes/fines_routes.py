from fastapi import APIRouter, HTTPException
from typing import List
from database import database
from schemas.fines import Fines
from crud.fines_crud import (
    get_fine, create_fine, update_fine, delete_fine, get_fines_by_loan
)

router = APIRouter(prefix="/api/fines", tags=["Fines"])

# GET one fine by FineID
@router.get("/{FineID}", response_model=Fines)
async def api_get_fine(FineID: int):
    async with database:
        fine = await get_fine(FineID)
        if not fine:
            raise HTTPException(status_code=404, detail="Fine not found")
        return Fines(**fine)
    
# POST: Create new fine
@router.post("/", response_model=Fines)
async def api_create_fine(fine: Fines):
    async with database:
        new_fine_id = await create_fine(fine.FineID, fine.LoanID, fine.Amount, fine.Paid)
        return Fines(**fine.dict())

# PUT: Update existing fine
@router.put("/", response_model=Fines)
async def api_update_fine(fine: Fines):
    async with database:
        try:
            await update_fine(fine.FineID, fine.LoanID, fine.Amount, fine.Paid)
            return fine
        except ValueError as err:
            raise HTTPException(status_code=400, detail=str(err))

# DELETE: Delete a single fine
@router.delete("/{FineID}")
async def api_delete_fine(FineID: int):
    async with database:
        deleted = await delete_fine(FineID)
        if not deleted:
            raise HTTPException(status_code=404, detail="Fine not found")
        return {"detail": f"Fine '{FineID}' deleted"}

# GET fines by LoanID
@router.get("/loan/{LoanID}", response_model=List[Fines])
async def api_get_fines_by_loan(LoanID: int):
    async with database:
        rows = await get_fines_by_loan(LoanID)
        return [Fines(**dict(r)) for r in rows]