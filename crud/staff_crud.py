from database import database

# READ all staff with pagination
async def get_staff(skip: int = 0, limit: int = 10):
    query = """
        SELECT StaffID, StaffName, Position, WorkTime
        FROM Staff
        LIMIT :limit OFFSET :skip
    """
    return await database.fetch_all(query=query, values={'limit': limit, 'skip': skip})

# READ one staff by StaffID
async def get_staff_member(StaffID: int):
    query = """
        SELECT StaffID, StaffName, Position, WorkTime
        FROM Staff
        WHERE StaffID = :StaffID
    """
    row = await database.fetch_one(query=query, values={"StaffID": StaffID})
    return dict(row) if row else None

# CREATE new staff member
async def create_staff(StaffID: int, StaffName: str, Position: str = None, WorkTime: int = None) -> int:
    query = """
        INSERT INTO Staff (StaffID, StaffName, Position, WorkTime)
        VALUES (:StaffID, :StaffName, :Position, :WorkTime)
    """
    try:
        await database.execute(query=query, values={
            "StaffID": StaffID,
            "StaffName": StaffName,
            "Position": Position,
            "WorkTime": WorkTime
        })
        return StaffID
    except Exception:
        raise ValueError(f"Staff member with ID {StaffID} already exists or invalid data.")
    
# UPDATE staff member
async def update_staff(StaffID: int, StaffName: str, Position: str, WorkTime: int) -> bool:
    query = """
        UPDATE Staff 
        SET StaffName = :StaffName, Position = :Position, WorkTime = :WorkTime
        WHERE StaffID = :StaffID
    """
    try:
        await database.execute(query=query, values={
            "StaffID": StaffID,
            "StaffName": StaffName,
            "Position": Position,
            "WorkTime": WorkTime
        })
        return True
    except Exception as err:
        raise ValueError(f"Error updating staff member {StaffID}: {err}")
    
# DELETE staff member
async def delete_staff(StaffID: int) -> bool:
    query = """
        DELETE FROM Staff 
        WHERE StaffID = :StaffID
    """
    try:
        await database.execute(query=query, values={"StaffID": StaffID})
        return True
    except Exception as err:
        raise ValueError(f"Error deleting staff member {StaffID}: {err}")
    
