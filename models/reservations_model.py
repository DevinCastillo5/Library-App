from sqlalchemy import Column, Integer, Date, CHAR
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Reservation(Base):
    __tablename__ = "Reservations"

    ReservationID = Column(Integer, primary_key=True)
    DateFor = Column(Date)
    MemberID = Column(Integer)
    BookReserved = Column(CHAR(13))
