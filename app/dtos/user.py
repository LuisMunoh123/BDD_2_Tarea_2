"""Data Transfer Objects for User endpoints."""

from advanced_alchemy.extensions.litestar import SQLAlchemyDTO, SQLAlchemyDTOConfig

from app.models import User


class UserReadDTO(SQLAlchemyDTO[User]):
    """DTO for reading user data without password."""

    config = SQLAlchemyDTOConfig(exclude={"admin"})


class UserCreateDTO(SQLAlchemyDTO[User]):
    """DTO for creating users."""

    config = SQLAlchemyDTOConfig(
        exclude={"id", "created_at", "updated_at", "loans"},
    )


class UserUpdateDTO(SQLAlchemyDTO[User]):
    """DTO for updating users with partial data."""

    config = SQLAlchemyDTOConfig(
        exclude={"id", "created_at", "password", "loans"},
        partial=True,
    )


class UserLoginDTO(SQLAlchemyDTO[User]):
    """DTO for user login."""

    config = SQLAlchemyDTOConfig(include={"username", "password"})
