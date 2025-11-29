from database import database
from datetime import date

# READ all reservations with pagination
async def get_reservations(skip: int = 0, limit: int = 10):
    query = """
        SELECT reservationID, DateFor, memberID, BookReserved
        FROM Reservations
        LIMIT :limit OFFSET :skip
    """
    return await database.fetch_all(query=query, values={'limit': limit, 'skip': skip})

# READ one reservation by reservationID
async def get_reservation(reservationID: int):
    query = """
        SELECT reservationID, DateFor, memberID, BookReserved
        FROM Reservations
        WHERE reservationID = :reservationID
    """
    row = await database.fetch_one(query=query, values={"reservationID": reservationID})
    return dict(row) if row else None

# CREATE new reservation
async def create_reservation(reservationID: int, DateFor: str, memberID: int, BookReserved: str) -> int:
    query = """
        INSERT INTO Reservations (reservationID, DateFor, memberID, BookReserved)
        VALUES (:reservationID, :DateFor, :memberID, :BookReserved)
    """
    try:
        await database.execute(query=query, values={
            "reservationID": reservationID,
            "DateFor": DateFor,
            "memberID": memberID,
            "BookReserved": BookReserved
        })
        return reservationID
    except Exception:
        raise ValueError(f"Reservation with ID {reservationID} already exists or invalid data.")
    
# UPDATE reservation
async def update_reservation(reservationID: int, DateFor: date, memberID: int, BookReserved: int) -> bool:
    query = """
        UPDATE Reservations 
        SET DateFor = :DateFor, memberID = :memberID, BookReserved = :BookReserved
        WHERE reservationID = :reservationID
    """
    try:
        await database.execute(query=query, values={
            "reservationID": reservationID,
            "DateFor": DateFor,
            "memberID": memberID,
            "BookReserved": BookReserved
        })
        return True
    except Exception as err:
        raise ValueError(f"Error updating reservation {reservationID}: {err}")
    
# DELETE reservation
async def delete_reservation(reservationID: int) -> bool:
    query = """
        DELETE FROM Reservations 
        WHERE reservationID = :reservationID
    """
    try:
        await database.execute(query=query, values={"reservationID": reservationID})
        return True
    except Exception as err:
        raise ValueError(f"Error deleting reservation {reservationID}: {err}")

# READ reservations by MemberID
async def get_reservations_by_member(memberID: int, skip: int = 0, limit: int = 10):
    query = """
        SELECT reservationID, DateFor, memberID, BookReserved
        FROM Reservations
        WHERE memberID = :memberID
        LIMIT :limit OFFSET :skip
    """
    return await database.fetch_all(query=query, values={'memberID': memberID, 'limit': limit, 'skip': skip})