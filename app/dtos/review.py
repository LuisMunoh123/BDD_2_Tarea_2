"""Data Transfer Objects for Review endpoints."""

from advanced_alchemy.extensions.litestar import SQLAlchemyDTO, SQLAlchemyDTOConfig

from app.models import Review


class ReviewReadDTO(SQLAlchemyDTO[Review]):
    """DTO for reading review data."""

    # Incluir user y book como pide el enunciado
    config = SQLAlchemyDTOConfig(
        include={"id", "rating", "comment", "review_date", "user", "book"},
    )


class ReviewCreateDTO(SQLAlchemyDTO[Review]):
    """DTO for creating reviews."""

    config = SQLAlchemyDTOConfig(
        exclude={
            "id",
            "created_at",
            "updated_at",
            "user",   # relaciones fuera del body
            "book",
        },
    )


class ReviewUpdateDTO(SQLAlchemyDTO[Review]):
    """DTO for updating reviews with partial data."""

    config = SQLAlchemyDTOConfig(
        exclude={
            "id",
            "created_at",
            "updated_at",
            "user",
            "book",
        },
        partial=True,
    )
