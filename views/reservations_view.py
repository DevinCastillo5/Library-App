import logging
from typing import Any, List, Optional
from starlette.requests import Request
from starlette_admin import BaseModelView
from starlette_admin.exceptions import FormValidationError
from starlette_admin.fields import StringField, DateField
from crud.reservations_crud import *
from database import database

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class ReservationsView(BaseModelView):
    # ===================================================================
    # BASIC CONFIGURATION
    # ===================================================================
    identity = "reservations"
    name = "Reservation"
    label = "Reservations"
    icon = "fa fa-user"
    pk_attr = "ReservationID"

    form_include_pk = True

    searchable_fields = ["ReservationID", "memberID"]
    sortable_fields = ["ReservationID", "ReservationDate"]

    # ===================================================================
    # FIELD DEFINITIONS
    # ===================================================================
    fields = [
        StringField(name="ReservationID", label="Reservation ID", required=True),
        DateField(name="DateFor", label="Date For", required=False),
        StringField(name="memberID", label="Member ID", required=False),
        StringField(name="BookReserved", label="Book Reserved", required=False),
    ]

    # ===================================================================
    # EXTRACT PRIMARY KEY VALUE
    # ===================================================================
    async def get_pk_value(self, request: Request, obj: Any) -> Any:
        return obj["ReservationID"] if isinstance(obj, dict) else getattr(obj, self.pk_attr)
    
    # ===================================================================
    # SERIALIZE
    # ===================================================================
    async def serialize(self, *args, **kwargs) -> dict:
        obj = args[0] if args else kwargs.get("obj") or kwargs.get("instance")
        if obj is None:
            return {}

        if not isinstance(obj, dict):
            obj = dict(obj._mapping) if hasattr(obj, "_mapping") else obj.__dict__

        return {
            "ReservationID": obj.get("ReservationID"),
            "DateFor": obj.get("DateFor"),
            "memberID": obj.get("memberID"),
            "BookReserved": obj.get("BookReserved"),
            "_meta": {"pk": obj.get("ReservationID")},
        }
    
    # ===================================================================
    # VALIDATE FORM INPUT
    # ===================================================================
    async def validate(self, request: Request, data: dict) -> None:
        errors = {}
        if not data.get("ReservationID"):
            errors["ReservationID"] = "Required"
        if not data.get("memberID"):
            errors["memberID"] = "Required"
        if not data.get("DateFor"):
            errors["DateFor"] = "Required"
        if not data.get("BookReserved"):
            errors["BookReserved"] = "Required"
        if errors:
            raise FormValidationError(errors)
        
    # ===================================================================
    # LIST VIEW WITH SEARCH
    # ===================================================================
    async def find_all(
        self,
        request: Request,
        skip: int = 0,
        limit: int = 100,
        where: Optional[Any] = None,
        order_by: Optional[List[Any]] = None,
    ) -> List[Any]:
        async with database:
            if where and isinstance(where, (str, int)) and str(where).strip():
                search_term = str(where).strip()
                query = """
                    SELECT ReservationID, DateFor, memberID, BookReserved
                    FROM Reservations
                    WHERE ReservationID LIKE :search OR memberID LIKE :search
                    LIMIT :limit OFFSET :skip
                """
                rows = await database.fetch_all(
                    query=query,
                    values={"search": f"%{search_term}%", "limit": limit, "skip": skip},
                )
            else:
                query = """
                    SELECT ReservationID, DateFor, memberID, BookReserved
                    FROM Reservations
                    LIMIT :limit OFFSET :skip
                """
                rows = await database.fetch_all(
                    query=query, values={"limit": limit, "skip": skip}
                )
            return [dict(row) for row in rows]
        
    # ===================================================================
    # COUNT TOTAL RECORDS
    # ===================================================================
    async def count(self, request: Request, where: Optional[Any] = None) -> int:
        async with database:
            if where and isinstance(where, (str, int)) and str(where).strip():
                search_term = str(where).strip()
                query = """
                    SELECT COUNT(*) FROM Reservations
                    WHERE ReservationID LIKE :search OR memberID LIKE :search
                """
                return await database.fetch_val(query, values={"search": f"%{search_term}%"})
            else:
                return await database.fetch_val("SELECT COUNT(*) FROM Reservations")
            
    # ===================================================================
    # FIND BY PRIMARY KEY
    # ===================================================================
    async def find_by_pk(self, request: Request, pk: Any) -> Optional[Any]:
        async with database:
            return await get_reservation(pk)
        
    # ===================================================================
    # CREATE NEW RESERVATION
    # ===================================================================
    async def create(self, request: Request, data: dict) -> Any:
        await self.validate(request, data)
        async with database:
            await create_reservation(data["ReservationID"], data.get("DateFor"), data.get("memberID"), data.get("BookReserved"))
            return await get_reservation(data["ReservationID"])

    # ===================================================================
    # UPDATE EXISTING RESERVATION
    # ===================================================================
    async def edit(self, request: Request, pk: Any, data: dict) -> Any:
        await self.validate(request, data)
        async with database:
            await update_reservation(pk, data.get("DateFor"), data.get("memberID"), data.get("BookReserved"))
            return await get_reservation(pk)

    # ===================================================================
    # DELETE ONE RESERVATION
    # ===================================================================
    async def delete(self, request: Request, pks: List[Any]) -> int:
        async with database:
            return await delete_reservation(pks)