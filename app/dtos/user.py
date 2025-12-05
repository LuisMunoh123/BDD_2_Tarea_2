"""Data Transfer Objects for User endpoints."""

from advanced_alchemy.extensions.litestar import SQLAlchemyDTO, SQLAlchemyDTOConfig

from app.models import User


class UserReadDTO(SQLAlchemyDTO[User]):
    """DTO para leer usuarios (respuesta)."""

    config = SQLAlchemyDTOConfig(
        exclude={
            "password",
            "loans",
            "reviews",
            "created_at",
            "updated_at",
        },
    )


class UserCreateDTO(SQLAlchemyDTO[User]):
    """DTO para crear usuarios."""

    config = SQLAlchemyDTOConfig(
        exclude={
            "id",
            "created_at",
            "updated_at",
            "loans",
            "reviews",
            "is_active",
        },
    )


class UserUpdateDTO(SQLAlchemyDTO[User]):
    """DTO para actualizar usuarios (parcial)."""

    config = SQLAlchemyDTOConfig(
        exclude={
            "id",
            "created_at",
            "updated_at",
            "loans",
            "reviews",
            "is_active",
        },
        partial=True,
    )


class UserLoginDTO(SQLAlchemyDTO[User]):
    """DTO for user login."""

    config = SQLAlchemyDTOConfig(include={"username", "password"})
