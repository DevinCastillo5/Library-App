import logging
from typing import Any, List, Optional
from starlette.requests import Request
from starlette_admin import BaseModelView
from starlette_admin.exceptions import FormValidationError
from starlette_admin.fields import IntegerField, StringField, DateField
from crud.loans_crud import *
from database import database

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class LoansView(BaseModelView):
    # ===================================================================
    # BASIC CONFIGURATION
    # ===================================================================
    identity = "loans"
    name = "Loan"
    label = "Loans"
    icon = "fa fa-handshake"
    pk_attr = "LoanID"

    form_include_pk = True

    searchable_fields = ["LoanID"]
    sortable_fields = ["LoanID", "ReturnDate", "ISBN", "MemberID", "StaffID", "CopyID"]

    # ===================================================================
    # FIELD DEFINITIONS
    # ===================================================================
    fields = [
        IntegerField(name="LoanID", label="Loan ID", required=True),
        DateField(name="ReturnDate", label="Return Date", required=False),
        StringField(name="ISBN", label="Book ISBN", required=False),
        IntegerField(name="MemberID", label="Member ID", required=False),
        IntegerField(name="StaffID", label="Staff ID", required=False),
        IntegerField(name="CopyID", label="Copy ID", required=False),
    ]

    # ===================================================================
    # EXTRACT PRIMARY KEY VALUE
    # ===================================================================
    async def get_pk_value(self, request: Request, obj: Any) -> Any:
        return obj["LoanID"] if isinstance(obj, dict) else getattr(obj, self.pk_attr)

    # ===================================================================
    # SERIALIZE OBJECT
    # ===================================================================
    async def serialize(self, *args, **kwargs) -> dict:
        obj = args[0] if args else kwargs.get("obj") or kwargs.get("instance")
        if obj is None:
            return {}

        if not isinstance(obj, dict):
            obj = dict(obj._mapping) if hasattr(obj, "_mapping") else obj.__dict__

        async with database:
            book_title = None
            member_name = None
            staff_name = None
            copy_location = None

            if obj.get("ISBN"):
                book = await database.fetch_one("SELECT Title FROM Books WHERE ISBN = :isbn", values={"isbn": obj["ISBN"]})
                book_title = book["Title"] if book else None

            if obj.get("MemberID"):
                member = await database.fetch_one("SELECT MemberName FROM Members WHERE MemberID = :id", values={"id": obj["MemberID"]})
                member_name = member["MemberName"] if member else None

            if obj.get("StaffID"):
                staff = await database.fetch_one("SELECT StaffName FROM Staff WHERE StaffID = :id", values={"id": obj["StaffID"]})
                staff_name = staff["StaffName"] if staff else None

            if obj.get("CopyID"):
                copy = await database.fetch_one("SELECT ShelfLocation FROM Copies WHERE CopyID = :id", values={"id": obj["CopyID"]})
                copy_location = copy["ShelfLocation"] if copy else None

        return {
            "LoanID": obj.get("LoanID"),
            "ReturnDate": obj.get("ReturnDate"),
            "ISBN": obj.get("ISBN"),
            "BookTitle": book_title,
            "MemberID": obj.get("MemberID"),
            "MemberName": member_name,
            "StaffID": obj.get("StaffID"),
            "StaffName": staff_name,
            "CopyID": obj.get("CopyID"),
            "CopyLocation": copy_location,
            "_meta": {"pk": obj.get("LoanID")},
        }

    # ===================================================================
    # VALIDATE FORM INPUT
    # ===================================================================
    async def validate(self, request: Request, data: dict) -> None:
        errors = {}
        if not data.get("LoanID"):
            errors["LoanID"] = "Required"

        async with database:
            if data.get("ISBN"):
                exists = await database.fetch_val("SELECT COUNT(*) FROM Books WHERE ISBN = :isbn", values={"isbn": data["ISBN"]})
                if exists == 0:
                    errors["ISBN"] = f"Book ISBN {data['ISBN']} does not exist"
            if data.get("MemberID"):
                exists = await database.fetch_val("SELECT COUNT(*) FROM Members WHERE MemberID = :id", values={"id": data["MemberID"]})
                if exists == 0:
                    errors["MemberID"] = f"Member ID {data['MemberID']} does not exist"
            if data.get("StaffID"):
                exists = await database.fetch_val("SELECT COUNT(*) FROM Staff WHERE StaffID = :id", values={"id": data["StaffID"]})
                if exists == 0:
                    errors["StaffID"] = f"Staff ID {data['StaffID']} does not exist"
            if data.get("CopyID"):
                exists = await database.fetch_val("SELECT COUNT(*) FROM Copies WHERE CopyID = :id", values={"id": data["CopyID"]})
                if exists == 0:
                    errors["CopyID"] = f"Copy ID {data['CopyID']} does not exist"

        if errors:
            raise FormValidationError(errors)

    # ===================================================================
    # LIST VIEW
    # ===================================================================
    async def find_all(self, request: Request, skip: int = 0, limit: int = 100, where: Optional[Any] = None, order_by: Optional[List[Any]] = None) -> List[Any]:
        async with database:
            rows = await get_loans(skip, limit)
            return [dict(row) for row in rows]

    # ===================================================================
    # COUNT TOTAL RECORDS
    # ===================================================================
    async def count(self, request: Request, where: Optional[Any] = None) -> int:
        async with database:
            return await database.fetch_val("SELECT COUNT(*) FROM Loans")

    # ===================================================================
    # FIND BY PRIMARY KEY
    # ===================================================================
    async def find_by_pk(self, request: Request, pk: Any) -> Optional[Any]:
        async with database:
            return await get_loan(pk)

    # ===================================================================
    # CREATE NEW LOAN
    # ===================================================================
    async def create(self, request: Request, data: dict) -> Any:
        await self.validate(request, data)
        async with database:
            await create_loan(
                loan_id=data["LoanID"],
                return_date=data.get("ReturnDate"),
                isbn=data.get("ISBN"),
                member_id=data.get("MemberID"),
                staff_id=data.get("StaffID"),
                copy_id=data.get("CopyID"),
            )
            return await get_loan(data["LoanID"])

    # ===================================================================
    # UPDATE EXISTING LOAN
    # ===================================================================
    async def edit(self, request: Request, pk: Any, data: dict) -> Any:
        await self.validate(request, data)
        async with database:
            await update_loan(
                loan_id=pk,
                return_date=data.get("ReturnDate"),
                isbn=data.get("ISBN"),
                member_id=data.get("MemberID"),
                staff_id=data.get("StaffID"),
                copy_id=data.get("CopyID"),
            )
            return await get_loan(pk)

    # ===================================================================
    # DELETE ONE OR MANY LOANS
    # ===================================================================
    async def delete(self, request: Request, pks: List[Any]) -> int:
        async with database:
            return await delete_loans(pks)
