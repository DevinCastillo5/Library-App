from fastapi import APIRouter, HTTPException
from database import database
from schemas.members import Members
from crud.members_crud import (get_members, get_member, create_member,
                              delete_member, update_member)

router = APIRouter(prefix="/api/members", tags=["Members"])

@router.get("/", response_model=list[Members])
async def api_get_members(skip: int = 0, limit: int = 10):
    async with database:
        rows = await get_members(skip, limit)
        return [Members(**dict(r)) for r in rows]

@router.get("/{member_id}", response_model=Members)
async def api_get_member(member_id: int):
    async with database:
        c = await get_member(member_id)
        if not c:
            raise HTTPException(404, "Member not found")
        return Members(**c)


@router.post("/", response_model=Members)
async def api_create_member(member: Members):
    async with database:
        try:
            code = await create_member(member.member_id, member.member_name, member.member_email, member.member_phone, member.member_address)
            return Members(**member.dict())
        except ValueError as err:
            raise HTTPException(status_code=400, detail=str(err))


@router.put("/", response_model=Members)
async def api_update_member(member: Members):
    async with database:
        try:
            await update_member(member.member_id, member.member_name, member.member_email, member.member_phone, member.member_address)
        except ValueError as err:
            raise HTTPException(status_code=400, detail=str(err))
        finally:
            return Members(**member.dict())

@router.delete("/{member_id}")
async def api_delete_member(member_id: int):
    async with database:
        deleted = await delete_member(member_id)
        if deleted == 0:
            raise HTTPException(404, "Course not found")
        return {"detail": "Course deleted"}
