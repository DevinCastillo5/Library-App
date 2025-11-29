import logging
from typing import Any, List, Optional
from starlette.requests import Request
from starlette_admin import BaseModelView
from starlette_admin.exceptions import FormValidationError
from starlette_admin.fields import StringField
from database import database
from crud.publishers_crud import (
    get_publisher,
    create_publisher,
    update_publisher,
    delete_publishers
)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class PublishersView(BaseModelView):
    identity = "publishers"
    name = "Publisher"
    label = "Publishers"
    icon = "fa fa-building"
    pk_attr = "publish_name"
    form_include_pk = True

    searchable_fields = ["publish_name"]
    sortable_fields = ["publish_name"]

    fields = [
        StringField(name="publish_name", label="Publisher Name", required=True),
        StringField(name="contact_info", label="Contact Info", required=False),
    ]


    async def get_pk_value(self, request: Request, obj: Any) -> Any:
        return obj["publish_name"] if isinstance(obj, dict) else getattr(obj, self.pk_attr)


    async def validate(self, request: Request, data: dict):
        errors = {}

        if not data.get("publish_name"):
            errors["publish_name"] = "Required"

        if errors:
            raise FormValidationError(errors)


    async def find_all(self, request: Request, skip: int = 0, limit: int = 100,
                       where: Optional[Any] = None, order_by=None):

        async with database:
            if where and str(where).strip():
                term = str(where).strip()
                query = """
                    SELECT * FROM Publishers
                    WHERE PublishName LIKE :s
                    LIMIT :limit OFFSET :skip
                """
                rows = await database.fetch_all(query, values={"s": f"%{term}%", "limit": limit, "skip": skip})
            else:
                rows = await database.fetch_all(
                    "SELECT * FROM Publishers LIMIT :limit OFFSET :skip",
                    values={"limit": limit, "skip": skip}
                )

        return [dict(r) for r in rows]


    async def count(self, request: Request, where: Optional[Any] = None):
        async with database:
            if where and str(where).strip():
                term = str(where).strip()
                return await database.fetch_val(
                    "SELECT COUNT(*) FROM Publishers WHERE PublishName LIKE :s",
                    values={"s": f"%{term}%"}
                )
            return await database.fetch_val("SELECT COUNT(*) FROM Publishers")


    async def find_by_pk(self, request: Request, pk: Any):
        async with database:
            return await get_publisher(pk)


    async def create(self, request: Request, data: dict):
        await self.validate(request, data)
        async with database:
            name = await create_publisher(
                data["publish_name"],
                data.get("contact_info")
            )
            return await get_publisher(name)


    async def edit(self, request: Request, pk: Any, data: dict):
        await self.validate(request, data)
        async with database:
            updated = await update_publisher(
                pk,
                data.get("contact_info")
            )
            if not updated:
                raise FormValidationError({"_schema": "Update failed"})
            return await get_publisher(pk)


    async def delete(self, request: Request, pks: List[Any]):
        async with database:
            return await delete_publishers(pks)
