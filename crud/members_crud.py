from database import database


# READ all with pagination
async def get_members(skip: int = 0, limit: int = 10):
    query = """
        SELECT memberID, memName, Email, Phone, Address
        FROM Members
        LIMIT :limit OFFSET :skip
    """
    return await database.fetch_all(query=query, values={'limit': limit, 'skip': skip})


# READ one by memberID
async def get_member(memberID: int):
    query = """
        SELECT memberID, memName, Email, Phone, Address
        FROM Members 
        WHERE memberID = :memberID
    """
    row = await database.fetch_one(query=query, values={"memberID": memberID})
    return dict(row) if row else None

# CREATE new course
async def create_member(memberID: int, memName: str, Email: str, Phone: str, Address: str) -> int:
    query = """
        INSERT INTO Members (memberID, memName, Email, Phone, Address)
        VALUES (:memberID, :memName, :Email, :Phone, :Address)
    """
    try:
        await database.execute(query=query, values={
            "memberID": memberID,
            "memName": memName,
            "Email": Email,
            "Phone": Phone,
            "Address": Address
        })
        return memberID
    except Exception:
        raise ValueError(f"Member with ID {memberID} already exists or invalid data.")

# UPDATE member
async def update_member(memberID: int, memName: str, Email: str, Phone: str, Address: str) -> bool:
    query = """
        UPDATE Members 
        SET memName = :memName, Email = :Email, Phone = :Phone, Address = :Address
        WHERE memberID = :memberID
    """
    try:
        await database.execute(query=query, values={
            "memberID": memberID,
            "memName": memName,
            "Email": Email,
            "Phone": Phone,
            "Address": Address
        })
        return True
    except Exception as err:
        raise ValueError(f"Error updating member {memberID}: {err}")

# DELETE one
async def delete_member(memberID: int) -> int:
    query = "DELETE FROM Members WHERE memberID = :memberID"
    return await database.execute(query=query, values={"memberID": memberID})


# DELETE many
async def delete_members(memberIDs: list[int]) -> int:
    if not memberIDs:
        return 0
    placeholders = ",".join(f":id{i}" for i in range(len(memberIDs)))
    query = f"DELETE FROM Members WHERE memberID IN ({placeholders})"
    values = {f"id{i}": memberID for i, memberID in enumerate(memberIDs)}
    return await database.execute(query=query, values=values)

