from database import database

# READ multiple
async def get_copies(skip: int = 0, limit: int = 10):
    query = """
    SELECT CopyID, ISBN, ShelfLocation, ConditionDesc
    FROM Copies
    LIMIT :limit OFFSET :skip
    """
    return await database.fetch_all(query=query, values={"limit": limit, "skip": skip})

# READ single
async def get_copy(CopyID: int):
    query = """
    SELECT CopyID, ISBN, ShelfLocation, ConditionDesc
    FROM Copies
    WHERE CopyID = :CopyID
    """
    row = await database.fetch_one(query=query, values={"CopyID": CopyID})
    return dict(row) if row else None

# CREATE
async def create_copy(CopyID: int, ISBN: str, ShelfLocation: str | None = None, ConditionDesc: str | None = None):
    query = """
    INSERT INTO Copies (CopyID, ISBN, ShelfLocation, ConditionDesc)
    VALUES (:CopyID, :ISBN, :ShelfLocation, :ConditionDesc)
    """
    try:
        await database.execute(query=query, values={
            "CopyID": CopyID,
            "ISBN": ISBN,
            "ShelfLocation": ShelfLocation,
            "ConditionDesc": ConditionDesc
        })
        return CopyID
    except Exception:
        raise ValueError(f"Copy with ID {CopyID} already exists.")

# UPDATE
async def update_copy(CopyID: int, ISBN: str, ShelfLocation: str | None = None, ConditionDesc: str | None = None):
    query = """
    UPDATE Copies
    SET ISBN = :ISBN, ShelfLocation = :ShelfLocation, ConditionDesc = :ConditionDesc
    WHERE CopyID = :CopyID
    """
    await database.execute(query=query, values={
        "CopyID": CopyID,
        "ISBN": ISBN,
        "ShelfLocation": ShelfLocation,
        "ConditionDesc": ConditionDesc
    })
    return True

# DELETE one
async def delete_copy(CopyID: int):
    query = "DELETE FROM Copies WHERE CopyID = :CopyID"
    return await database.execute(query=query, values={"CopyID": CopyID})

# DELETE many
async def delete_copies(CopyIDs: list[int]):
    if not CopyIDs:
        return 0
    placeholders = ', '.join([f":id{i}" for i in range(len(CopyIDs))])
    query = f"DELETE FROM Copies WHERE CopyID IN ({placeholders})"
    values = {f"id{i}": CopyIDs[i] for i in range(len(CopyIDs))}
    return await database.execute(query=query, values=values)
