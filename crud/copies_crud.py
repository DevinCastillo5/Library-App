from database import database

async def get_copies(skip: int = 0, limit: int = 10):
    query="""
        SELECT CopyID, ISBN, Condition
        FROM Copies
        LIMIT :limit OFFSET :skip
        """
    return await database.fetch_all(query=query, values={'limit': limit, 'skip': skip})

# READ one: Get single copy by CopyID
async def get_copy(CopyID: int):
    query = """
    SELECT CopyID, ISBN, Condition
    FROM Copies WHERE CopyID = :CopyID
    """
    row = await database.fetch_one(query=query, values={"CopyID": CopyID})
    return dict(row) if row else None  # Convert Row → dict for Pydantic

# CREATE: Insert a new copy. Returns the CopyID (PK).
# :param tells type checkers what each argument is — improves code clarity and IDE help.
async def create_copy(CopyID: int, ISBN: str, Condition: str) -> int:
    query = """
    INSERT INTO Copies (CopyID, ISBN, Condition)
    VALUES (:CopyID, :ISBN, :Condition)
    """
    try:
        # Execute the insert using named parameters (:name) — safe from SQL injection
        await database.execute(query=query, values={
            "CopyID": CopyID,
            "ISBN": ISBN,
            "Condition": Condition
        })
        return CopyID  # Return PK so API can confirm creation
    except Exception:
        # Raise clear error if CopyID already exists (duplicate primary key)
        raise ValueError(f"Copy with ID {CopyID} already exists.")
    
# UPDATE
async def update_copy(CopyID: int, ISBN: str, Condition: str) -> bool:
    query = """
    UPDATE Copies SET ISBN = :ISBN, Condition = :Condition
    WHERE CopyID = :CopyID
    """
    try:
        await database.execute(query=query, values={
            "CopyID": CopyID,
            "ISBN": ISBN,
            "Condition": Condition
        })
        return True
    except Exception as err:
        raise ValueError(f"Error updating copy {CopyID}: {err}")
    
# DELETE one
async def delete_copy(CopyID: int) -> int:
    query = "DELETE FROM Copies WHERE CopyID = :CopyID"
    return await database.execute(query=query, values={"CopyID": CopyID})

# DELETE many
async def delete_copies(CopyIDs: list[int]) -> int:
    if not CopyIDs:
        return 0  # Nothing to delete
    placeholders = ', '.join([f":id{i}" for i in range(len(CopyIDs))])
    query = f"DELETE FROM Copies WHERE CopyID IN ({placeholders})"
    values = {f"id{i}": CopyIDs[i] for i in range(len(CopyIDs))}
    return await database.execute(query=query, values=values)