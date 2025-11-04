from litestar.app import Litestar
from litestar.openapi import OpenAPIConfig
from litestar.openapi.plugins import ScalarRenderPlugin, SwaggerRenderPlugin

from app.controllers.book import BookController
from app.controllers.user import UserController
from app.db import sqlalchemy_plugin

openapi_config = OpenAPIConfig(
    title="Mi API",
    version="0.1",
    render_plugins=[
        ScalarRenderPlugin(),
        SwaggerRenderPlugin(),
    ],
)

app = Litestar(
    route_handlers=[UserController, BookController],
    openapi_config=openapi_config,
    debug=True,
    plugins=[sqlalchemy_plugin],
)
