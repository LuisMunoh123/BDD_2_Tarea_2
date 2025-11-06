from litestar.connection import ASGIConnection
from litestar.contrib.jwt import OAuth2PasswordBearerAuth
from litestar.security.jwt import Token

from app.models import User
from app.repositories.user import UserRepository


async def retrieve_user_handler(token: Token, connection: ASGIConnection) -> User | None:
    from app.db import sqlalchemy_config

    with sqlalchemy_config.get_session() as session:
        users_repo = UserRepository(session=session)

        try:
            return users_repo.get_one(username=token.sub)
        except Exception:
            return None


oauth2_auth = OAuth2PasswordBearerAuth[User](
    retrieve_user_handler=retrieve_user_handler,
    token_secret="secret123",
    token_url="/auth/login",
    exclude=["/auth/login", "/schema"],
)
