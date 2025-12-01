import logging
from typing import Any, List, Optional
from starlette.requests import Request
from starlette_admin import BaseModelView
from starlette_admin.exceptions import FormValidationError
from starlette_admin.fields import StringField, DateField
from crud.fines_crud import *
from database import database

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class FinesView(BaseModelView):
    # ===================================================================
    # BASIC CONFIGURATION
    # ===================================================================
    identity = "fines"
    name = "Fines"
    label = "Fines"
    icon = "fa fa-user"
    pk_attr = "FineID"

    form_include_pk = True

    searchable_fields = ["FineID", "Amount"]
    sortable_fields = ["FineID", "Amount"]

    # ===================================================================
    # FIELD DEFINITIONS
    # ===================================================================
    fields = [
        StringField(name="FineID", label="Fine ID", required=True),
        StringField(name="Amount", label="Amount", required=False),
        StringField(name="DateIssued", label="Date Issued", required=False),
        StringField(name="DatePaid", label="Date Paid", required=False),
    ]


    # ===================================================================
    # EXTRACT PRIMARY KEY VALUE
    # ===================================================================
    async def get_pk_value(self, request: Request, obj: Any) -> Any:
        return obj["FineID"] if isinstance(obj, dict) else getattr(obj, self.pk_attr)

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
            "FineID": obj.get("FineID"),
            "Amount": obj.get("AmountFined"),
            "DaysOverdue": obj.get("DaysOverdue"),
            "LoanID": obj.get("LoanID"),
            "_meta": {"pk": obj.get("FineID")},
        }
    
    # ===================================================================
    # VALIDATE FORM INPUT
    # ===================================================================
    async def validate(self, request: Request, data: dict) -> None:
        errors = {}
        if not data.get("FineID"):
            errors["FineID"] = "Required"
        if not data.get("Amount"):
            errors["Amount"] = "Required"
        if not data.get("DaysOverdue"):
            errors["DaysOverdue"] = "Required"
        if not data.get("LoanID"):
            errors["LoanID"] = "Required"
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
                    SELECT FineID, Amount, DaysOverdue, LoanID
                    FROM Fines
                    WHERE FineID LIKE :search OR Amount LIKE :search
                    LIMIT :limit OFFSET :skip
                """
                rows = await database.fetch_all(
                    query=query,
                    values={"search": f"%{search_term}%", "limit": limit, "skip": skip},
                )
            else:
                query = """
                    SELECT FineID, Amount, DaysOverdue, LoanID
                    FROM Fines
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
                    SELECT COUNT(*) FROM Fines
                    WHERE FineID LIKE :search OR LoanID LIKE :search
                """
                return await database.fetch_val(query, values={"search": f"%{search_term}%"})
            else:
                return await database.fetch_val("SELECT COUNT(*) FROM Fines")

    # ===================================================================
    # FIND BY PRIMARY KEY
    # ===================================================================
    async def find_by_pk(self, request: Request, pk: Any) -> Optional[Any]:
        async with database:
            return await get_fine(pk)
        
    # ===================================================================
    # CREATE NEW FINE
    # ===================================================================
    async def create(self, request: Request, data: dict) -> Any:
        await self.validate(request, data)
        async with database:
            await create_fine(data["FineID"], data.get("Amount"), data.get("DaysOverdue"), data.get("LoanID"))
            return await get_fine(data["FineID"])

    # ===================================================================
    # UPDATE EXISTING FINE
    # ===================================================================
    async def edit(self, request: Request, pk: Any, data: dict) -> Any:
        await self.validate(request, data)
        async with database:
            await update_fine(pk, data.get("Amount"), data.get("DaysOverdue"), data.get("LoanID"))
            return await get_fine(pk)
    
    # ===================================================================
    # DELETE ONE FINE
    # ===================================================================
    async def delete(self, request: Request, pks: List[Any]) -> int:
        async with database:
            return await delete_fine(pks)
        
    # ===================================================================
    # READ FINE BY LOAN ID
    # ===================================================================
    async def get_fines_by_loan(self, request: Request, LoanID: int) -> List[Any]:
        async with database:
            rows = await get_fines_by_loan(LoanID)
            return [dict(row) for row in rows]