"""Database configuration with SQLAlchemy."""

from advanced_alchemy.extensions.litestar import SQLAlchemyPlugin, SQLAlchemySyncConfig

sqlalchemy_config = SQLAlchemySyncConfig(
    connection_string="sqlite:///db.sqlite3",
    create_all=True,
)

sqlalchemy_plugin = SQLAlchemyPlugin(config=sqlalchemy_config)
