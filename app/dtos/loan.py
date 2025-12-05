"""Data Transfer Objects for Loan endpoints."""

from advanced_alchemy.extensions.litestar import SQLAlchemyDTO, SQLAlchemyDTOConfig

from app.models import Loan


class LoanReadDTO(SQLAlchemyDTO[Loan]):
    config = SQLAlchemyDTOConfig(
        exclude={"created_at", "updated_at"},
    )


class LoanCreateDTO(SQLAlchemyDTO[Loan]):
    config = SQLAlchemyDTOConfig(
        exclude={
            "id",
            "created_at",
            "updated_at",
            "user",
            "book",
            "due_date",
            "fine_amount",
            "status",
            "return_dt",
        },
    )


class LoanUpdateDTO(SQLAlchemyDTO[Loan]):
    config = SQLAlchemyDTOConfig(
        include={"status"},
        partial=True,
    )
