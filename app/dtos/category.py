"""Data Transfer Objects for Category endpoints."""

from advanced_alchemy.extensions.litestar import SQLAlchemyDTO, SQLAlchemyDTOConfig

from app.models import Category


class CategoryReadDTO(SQLAlchemyDTO[Category]):
    """DTO para leer categorías."""

    config = SQLAlchemyDTOConfig(
        exclude={"created_at", "updated_at", "books"},
    )


class CategoryCreateDTO(SQLAlchemyDTO[Category]):
    """DTO para crear categorías."""

    config = SQLAlchemyDTOConfig(
        exclude={"id", "created_at", "updated_at", "books"},
    )


class CategoryUpdateDTO(SQLAlchemyDTO[Category]):
    """DTO para actualizar categorías (parcial)."""

    config = SQLAlchemyDTOConfig(
        exclude={"id", "created_at", "updated_at", "books"},
        partial=True,
    )
