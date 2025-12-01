from fastapi import APIRouter, HTTPException
from database import database
from schemas.publishers import Publishers
from crud.publishers_crud import (get_publishers, get_publisher, create_publisher,
                                  delete_publisher, update_publisher, delete_publishers)

router = APIRouter(prefix="/api/publishers", tags=["Publishers"])

@router.get("/", response_model=list[Publishers])
async def api_get_publishers(skip: int = 0, limit: int = 10):
    async with database:
        rows = await get_publishers(skip, limit)
        return [Publishers(**dict(r)) for r in rows]
    
@router.get("/{publish_name}", response_model=Publishers)
async def api_get_publisher(publish_name: str):
    async with database:
        p = await get_publisher(publish_name)
        if not p:
            raise HTTPException(404, "Publisher not found")
        return Publishers(**p)
    
@router.post("/", response_model=Publishers)
async def api_create_publisher(publisher: Publishers):
    async with database:
        try:
            code = await create_publisher(publisher.PublishName, publisher.ContactInfo)
            return Publishers(**publisher.dict())
        except ValueError as err:
            raise HTTPException(status_code=400, detail=str(err))
        
@router.put("/", response_model=Publishers)
async def api_update_publisher(publisher: Publishers):
    async with database:
        try:
            await update_publisher(publisher.PublishName, publisher.ContactInfo)
        except ValueError as err:
            raise HTTPException(status_code=400, detail=str(err))
        finally:
            return Publishers(**publisher.dict())
        
@router.delete("/{publish_name}")
async def api_delete_publisher(publish_name: str):
    async with database:
        deleted = await delete_publisher(publish_name)
        if deleted == 0:
            raise HTTPException(404, "Publisher not found")
        return {"detail": "Publisher deleted"}
    
@router.delete("/")
async def api_delete_publishers(publish_names: list[str]):
    async with database:
        if not publish_names:
            raise HTTPException(status_code=400, detail="No publisher names provided for deletion.")
        deleted_count = await delete_publishers(publish_names)
        return {"detail": f"Deleted {deleted_count} publishers."}
    if not PublishNames:
        return 0  # Nothing to delete
    query = "DELETE FROM Publishers WHERE PublishName IN :PublishNames"
    return await database.execute(query=query, values={"PublishNames": PublishNames})   