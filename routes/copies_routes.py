from fastapi import APIRouter, HTTPException
from database import database
from schemas.copies import Copies
from crud.copies_crud import (get_copies, get_copy, create_copy,
                              delete_copy, update_copy, delete_copies)

router = APIRouter(prefix="/api/copies", tags=["Copies"])

@router.get("/", response_model=list[Copies])
async def api_get_copies(skip: int = 0, limit: int = 10):
    async with database:
        rows = await get_copies(skip, limit)
        return [Copies(**dict(r)) for r in rows]
    
@router.get("/{copy_id}", response_model=Copies)
async def api_get_copy(copy_id: int):
    async with database:
        c = await get_copy(copy_id)
        if not c:
            raise HTTPException(404, "Copy not found")
        return Copies(**c)
    
@router.post("/", response_model=Copies)
async def api_create_copy(copy: Copies):
    async with database:
        try:
            code = await create_copy(copy.CopyID, copy.ISBN, copy.Condition)
            return Copies(**copy.dict())
        except ValueError as err:
            raise HTTPException(status_code=400, detail=str(err))
        
@router.put("/", response_model=Copies)
async def api_update_copy(copy: Copies):
    async with database:
        try:
            await update_copy(copy.CopyID, copy.ISBN, copy.Condition)
        except ValueError as err:
            raise HTTPException(status_code=400, detail=str(err))
        finally:
            return Copies(**copy.dict())
        
@router.delete("/{copy_id}")
async def api_delete_copy(copy_id: int):
    async with database:
        deleted = await delete_copy(copy_id)
        if deleted == 0:
            raise HTTPException(404, "Copy not found")
        return {"detail": "Copy deleted"}
    
@router.delete("/")
async def api_delete_copies(copy_ids: list[int]):
    async with database:
        if not copy_ids:
            raise HTTPException(status_code=400, detail="No copy IDs provided for deletion.")
        deleted_count = await delete_copies(copy_ids)
        return {"detail": f"Deleted {deleted_count} copies."}   
    if not CopyIDs:
        return 0  # Nothing to delete
    placeholders = ', '.join([f":id{i}" for i in range(len(CopyIDs))])
    query = f"DELETE FROM Copies WHERE CopyID IN ({placeholders})"
    values = {f"id{i}": CopyIDs[i] for i in range(len(CopyIDs))}
    return await database.execute(query=query, values=values)   