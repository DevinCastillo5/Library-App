from database import database

# READ all fines with pagination
async def get_fines(skip: int = 0, limit: int = 10):
    query = """
        SELECT FineID, AmountFined, DaysOverdue, LoanID
        FROM Fines
        LIMIT :limit OFFSET :skip
    """
    return await database.fetch_all(query=query, values={'limit': limit, 'skip': skip})

# READ one fine by FineID
async def get_fine(FineID: int):
    query = """
        SELECT FineID, AmountFined, DaysOverdue, LoanID
        FROM Fines
        WHERE FineID = :FineID
    """
    row = await database.fetch_one(query=query, values={"FineID": FineID})
    return dict(row) if row else None

# CREATE new fine
async def create_fine(FineID: int, AmountFined: int, DaysOverdue: int, LoanID: int) -> int:
    query = """
        INSERT INTO Fines (FineID, AmountFined, DaysOverdue, LoanID)
        VALUES (:FineID, :AmountFined, :DaysOverdue, :LoanID)
    """
    try:
        await database.execute(query=query, values={
            "FineID": FineID,
            "AmountFined": AmountFined,
            "DaysOverdue": DaysOverdue,
            "LoanID": LoanID
        })
        return FineID
    except Exception:
        raise ValueError(f"Fine with ID {FineID} already exists or invalid data.")
    
# UPDATE fine
async def update_fine(FineID: int, AmountFined: int, DaysOverdue: int, LoanID: int) -> bool:
    query = """
        UPDATE Fines 
        SET AmountFined = :AmountFined, DaysOverdue = :DaysOverdue, LoanID = :LoanID
        WHERE FineID = :FineID
    """
    try:
        await database.execute(query=query, values={
            "FineID": FineID,
            "AmountFined": AmountFined,
            "DaysOverdue": DaysOverdue,
            "LoanID": LoanID
        })
        return True
    except Exception as err:
        raise ValueError(f"Error updating fine {FineID}: {err}")
    
# DELETE fine
async def delete_fine(FineID: int) -> bool:
    query = """
        DELETE FROM Fines 
        WHERE FineID = :FineID
    """
    try:
        await database.execute(query=query, values={"FineID": FineID})
        return True
    except Exception as err:
        raise ValueError(f"Error deleting fine {FineID}: {err}")
    
# READ fines by LoanID
async def get_fines_by_loan(LoanID: int):
    query = """
        SELECT FineID, AmountFined, DaysOverdue, LoanID
        FROM Fines
        WHERE LoanID = :LoanID
    """
    return await database.fetch_all(query=query, values={"LoanID": LoanID})