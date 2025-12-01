import logging
from typing import Any, List, Optional
from starlette.requests import Request
from starlette_admin import BaseModelView
from starlette_admin.exceptions import FormValidationError
from starlette_admin.fields import IntegerField, StringField
from database import database
from crud.copies_crud import (
    get_copy,
    create_copy,
    update_copy,
    delete_copies
)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class CopiesView(BaseModelView):
    # ===================================================================
    # BASIC CONFIGURATION
    # ===================================================================
    identity = "copies"
    name = "Copy"
    label = "Copies"
    icon = "fa fa-copy"
    pk_attr = "copy_id"
    form_include_pk = True

    searchable_fields = ["isbn"]
    sortable_fields = ["copy_id", "isbn", "shelf_location"]


    # ===================================================================
    # FIELD DEFINITIONS
    # ===================================================================
    fields = [
        IntegerField(name="copy_id", label="Copy ID", required=True),
        StringField(name="isbn", label="ISBN", required=True),
        StringField(name="shelf_location", label="Shelf Location", required=False),
        StringField(name="condition_desc", label="Condition", required=False),
    ]

    # ===================================================================
    # EXTRACT PRIMARY KEY VALUE
    # ===================================================================
    async def get_pk_value(self, request: Request, obj: Any) -> Any:
        return obj["copy_id"] if isinstance(obj, dict) else getattr(obj, self.pk_attr)

    # ===================================================================
    # VALIDATE FORM DATA
    # ===================================================================
    async def validate(self, request: Request, data: dict):
        errors = {}

        if not data.get("copy_id"):
            errors["copy_id"] = "Required"
        if not data.get("isbn"):
            errors["isbn"] = "Required"

        # Validate FK: ISBN exists
        async with database:
            exists = await database.fetch_val(
                "SELECT COUNT(*) FROM Books WHERE ISBN=:isbn",
                values={"isbn": data["isbn"]}
            )
            if exists == 0:
                errors["isbn"] = f"Book ISBN {data['isbn']} does not exist"

        if errors:
            raise FormValidationError(errors)


    async def find_all(self, request: Request, skip: int = 0, limit: int = 100,
                       where: Optional[Any] = None, order_by=None):

        async with database:
            if where and str(where).strip():
                term = str(where).strip()
                query = """
                    SELECT * FROM Copies
                    WHERE ISBN LIKE :s
                    LIMIT :limit OFFSET :skip
                """
                rows = await database.fetch_all(
                    query, values={"s": f"%{term}%", "limit": limit, "skip": skip}
                )
            else:
                rows = await database.fetch_all(
                    "SELECT * FROM Copies LIMIT :limit OFFSET :skip",
                    values={"limit": limit, "skip": skip}
                )

        return [dict(r) for r in rows]


    async def count(self, request: Request, where: Optional[Any] = None) -> int:
        async with database:
            if where and str(where).strip():
                term = str(where).strip()
                return await database.fetch_val(
                    "SELECT COUNT(*) FROM Copies WHERE ISBN LIKE :s",
                    values={"s": f"%{term}%"}
                )
            return await database.fetch_val("SELECT COUNT(*) FROM Copies")


    async def find_by_pk(self, request: Request, pk: Any):
        async with database:
            return await get_copy(pk)


    async def create(self, request: Request, data: dict):
        await self.validate(request, data)
        async with database:
            cid = await create_copy(
                data["copy_id"],
                data["isbn"],
                data.get("shelf_location"),
                data.get("condition_desc")
            )
            return await get_copy(cid)


    async def edit(self, request: Request, pk: Any, data: dict):
        await self.validate(request, data)
        async with database:
            updated = await update_copy(
                pk,
                data["isbn"],
                data.get("shelf_location"),
                data.get("condition_desc")
            )
            if not updated:
                raise FormValidationError({"_schema": "Update failed"})
            return await get_copy(pk)


    async def delete(self, request: Request, pks: List[Any]):
        async with database:
            return await delete_copies(pks)
