from fastapi import APIRouter, HTTPException
from typing import List
from schemas.members import Members
from crud.members_crud import get_members, get_member, create_member, update_member, delete_member

router = APIRouter(
    prefix="/api/members",
    tags=["Members"]
)

# Get all members
@router.get("/", response_model=List[Members])
async def api_get_members(skip: int = 0, limit: int = 100):
    return await get_members(skip, limit)

# Get a single member by memberID
@router.get("/{memberID}", response_model=Members)
async def api_get_member(memberID: int):
    member = await get_member(memberID)
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    return member

# Create a new member
@router.post("/", response_model=Members)
async def api_create_member(member: Members):
    return await create_member(member)

# Update a member
@router.put("/", response_model=Members)
async def api_update_member(member: Members):
    existing = await get_member(member.memberID)
    if not existing:
        raise HTTPException(status_code=404, detail="Member not found")
    return await update_member(member)

# Delete a member
@router.delete("/{memberID}")
async def api_delete_member(memberID: int):
    existing = await get_member(memberID)
    if not existing:
        raise HTTPException(status_code=404, detail="Member not found")
    await delete_member(memberID)
    return {"detail": "Member deleted"}
