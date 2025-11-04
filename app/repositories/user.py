from advanced_alchemy.repository import SQLAlchemySyncRepository
from sqlalchemy.orm import Session

from app.models import User


class UserRepository(SQLAlchemySyncRepository[User]):
    """Repository for user database operations."""

    model_type = User


async def provide_user_repo(db_session: Session) -> UserRepository:
    """Provide user repository instance with auto-commit."""
    return UserRepository(session=db_session, auto_commit=True)
