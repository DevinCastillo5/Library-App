from starlette_admin.contrib.sqla import ModelView
from models.reservations_model import Reservation  # <-- your SQLAlchemy model

class ReservationsView(ModelView):
    model = Reservation
    icon = "fa fa-handshake"
    label = "Reservations"
    name = "Reservations"

async def create(self, request: Request, data: dict) -> Any:
    print("Creating reservation with data:", data)  # Add this
    await self.validate(request, data)
    async with database:
        await create_reservation(data["ReservationID"], data.get("DateFor"), data.get("memberID"), data.get("BookReserved"))
        return await get_reservation(data["ReservationID"])
