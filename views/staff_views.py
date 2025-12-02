import logging
from typing import Any, List, Optional
from starlette.requests import Request
from starlette_admin import BaseModelView
from starlette_admin.exceptions import FormValidationError
from starlette_admin.fields import StringField, DateField
from crud.staff_crud import *
from database import database

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class StaffViews(BaseModelView):
    # ===================================================================
    # BASIC CONFIGURATION
    # ===================================================================
    identity = "staff"
    name = "Staff"
    label = "Staff"
    icon = "fa fa-user"
    pk_attr = "StaffID"

    form_include_pk = True

    searchable_fields = ["StaffID", "StaffName"]
    sortable_fields = ["StaffID", "StaffName"]

    # ===================================================================
    # FIELD DEFINITIONS
    # ===================================================================
    fields = [
        StringField(name="StaffID", label="Staff ID", required=True),
        StringField(name="StaffName", label="Staff Name", required=False),
        StringField(name="Position", label="Position", required=False),
        StringField(name="Email", label="Email", required=False),
    ]

    # ===================================================================
    # EXTRACT PRIMARY KEY VALUE
    # ===================================================================
    async def get_pk_value(self, request: Request, obj: Any) -> Any:
        return obj["StaffID"] if isinstance(obj, dict) else getattr(obj, self.pk_attr)
    
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
            "StaffID": obj.get("StaffID"),
            "StaffName": obj.get("StaffName"),
            "Position": obj.get("Position"),
            "Email": obj.get("Email"),
            "_meta": {"pk": obj.get("StaffID")},
        }

    # ===================================================================
    # VALIDATE FORM INPUT
    # ===================================================================
    async def validate(self, request: Request, data: dict) -> None:
        errors = {}
        if not data.get("StaffID"):
            errors["StaffID"] = "Required"
        if not data.get("StaffName"):
            errors["StaffName"] = "Required"
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
                    SELECT StaffID, StaffName, Position, Email
                    FROM Staff
                    WHERE StaffID LIKE :search OR StaffName LIKE :search
                    LIMIT :limit OFFSET :skip
                """
                rows = await database.fetch_all(
                    query=query,
                    values={"search": f"%{search_term}%", "limit": limit, "skip": skip},
                )
            else:
                query = """
                    SELECT StaffID, StaffName, Position, Email
                    FROM Staff
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
                    SELECT COUNT(*) FROM Staff
                    WHERE StaffID LIKE :search OR StaffName LIKE :search
                """
                return await database.fetch_val(query, values={"search": f"%{search_term}%"})
            else:
                return await database.fetch_val("SELECT COUNT(*) FROM Staff")
            
    # ===================================================================
    # FIND BY PRIMARY KEY
    # ===================================================================
    async def find_by_pk(self, request: Request, pk: Any) -> Optional[Any]:
        async with database:
            return await get_staff(pk)
        
    # ===================================================================
    # CREATE NEW STAFF
    # ===================================================================
    async def create(self, request: Request, data: dict) -> Any:
        await self.validate(request, data)
        async with database:
            await create_staff(data["StaffID"], data.get("StaffName"), data.get("Position"), data.get("Email"))
            return await get_staff(data["StaffID"])
        
    # ===================================================================
    # UPDATE EXISTING STAFF
    # ===================================================================
    async def edit(self, request: Request, pk: Any, data: dict) -> Any:
        await self.validate(request, data)
        async with database:
            await update_staff(pk, data.get("StaffName"), data.get("Position"), data.get("Email"))
            return await get_staff(pk)
        
    # ===================================================================
    # DELETE ONE STAFF
    # ===================================================================
    async def delete(self, request: Request, pks: List[Any]) -> int:
        async with database:
            return await delete_staff(pks)
        
