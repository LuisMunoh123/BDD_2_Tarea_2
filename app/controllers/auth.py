"""Controller for authentication endpoints."""

from typing import Annotated

from litestar import Controller, Response, post
from litestar.di import Provide
from litestar.enums import RequestEncodingType
from litestar.exceptions import HTTPException
from litestar.params import Body
from litestar.security.jwt import OAuth2Login

from app.dtos.user import UserLoginDTO
from app.models import User
from app.repositories.user import UserRepository, password_hasher, provide_user_repo
from app.security import oauth2_auth


class AuthController(Controller):
    """Controller for authentication operations."""

    path = "/auth"
    tags = ["auth"]

    @post(
        "/login",
        dependencies={"users_repo": Provide(provide_user_repo)},
        dto=UserLoginDTO,
    )
    async def login(
        self,
        data: Annotated[User, Body(media_type=RequestEncodingType.URL_ENCODED)],
        users_repo: UserRepository,
    ) -> Response[OAuth2Login]:
        """Authenticate user and generate OAuth2 token."""
        user = users_repo.get_one_or_none(username=data.username)

        if user is not None:
            if password_hasher.verify(data.password, user.password):
                return oauth2_auth.login(identifier=user.username)

        raise HTTPException(status_code=401, detail="Usuario o contraseña incorrectos")
