import logging
from typing import Any, List, Optional
from starlette.requests import Request
from starlette_admin import BaseModelView
from starlette_admin.exceptions import FormValidationError
from starlette_admin.fields import StringField, DateField
from crud.authors_crud import *
from database import database

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class AuthorsView(BaseModelView):
    # ===================================================================
    # BASIC CONFIGURATION
    # ===================================================================
    identity = "authors"
    name = "Author"
    label = "Authors"
    icon = "fa fa-user"
    pk_attr = "AuthorName"

    form_include_pk = True

    searchable_fields = ["AuthorName", "Nationality"]
    sortable_fields = ["AuthorName", "DOB", "Nationality"]

    # ===================================================================
    # FIELD DEFINITIONS
    # ===================================================================
    fields = [
        StringField(name="AuthorName", label="Author Name", required=True),
        DateField(name="DOB", label="Date of Birth", required=False),
        StringField(name="Nationality", label="Nationality", required=False),
    ]

    # ===================================================================
    # EXTRACT PRIMARY KEY VALUE
    # ===================================================================
    async def get_pk_value(self, request: Request, obj: Any) -> Any:
        return obj["AuthorName"] if isinstance(obj, dict) else getattr(obj, self.pk_attr)
    

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
            "AuthorName": obj.get("AuthorName"),
            "DOB": obj.get("DOB"),
            "Nationality": obj.get("Nationality"),
            "_meta": {"pk": obj.get("AuthorName")},
        }
    
    # ===================================================================
    # VALIDATE FORM INPUT
    # ===================================================================
    async def validate(self, request: Request, data: dict) -> None:
        errors = {}
        if not data.get("AuthorName"):
            errors["AuthorName"] = "Required"
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
                    SELECT AuthorName, DOB, Nationality
                    FROM Authors
                    WHERE AuthorName LIKE :search OR Nationality LIKE :search
                    LIMIT :limit OFFSET :skip
                """
                rows = await database.fetch_all(
                    query=query,
                    values={"search": f"%{search_term}%", "limit": limit, "skip": skip},
                )
            else:
                query = """
                    SELECT AuthorName, DOB, Nationality
                    FROM Authors
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
                    SELECT COUNT(*) FROM Authors
                    WHERE AuthorName LIKE :search OR Nationality LIKE :search
                """
                return await database.fetch_val(query, values={"search": f"%{search_term}%"})
            else:
                return await database.fetch_val("SELECT COUNT(*) FROM Authors")

    # ===================================================================
    # FIND BY PRIMARY KEY
    # ===================================================================
    async def find_by_pk(self, request: Request, pk: Any) -> Optional[Any]:
        async with database:
            return await get_author(pk)

    # ===================================================================
    # CREATE NEW AUTHOR
    # ===================================================================
    async def create(self, request: Request, data: dict) -> Any:
        await self.validate(request, data)
        async with database:
            await create_author(data["AuthorName"], data.get("DOB"), data.get("Nationality"))
            return await get_author(data["AuthorName"])

    # ===================================================================
    # UPDATE EXISTING AUTHOR
    # ===================================================================
    async def edit(self, request: Request, pk: Any, data: dict) -> Any:
        await self.validate(request, data)
        async with database:
            await update_author(pk, data.get("DOB"), data.get("Nationality"))
            return await get_author(pk)

    # ===================================================================
    # DELETE ONE OR MANY AUTHORS
    # ===================================================================
    async def delete(self, request: Request, pks: List[Any]) -> int:
        async with database:
            return await delete_authors(pks)