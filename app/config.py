"""Application configuration using Pydantic Settings."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Main application settings."""
    debug: bool = False
    jwt_secret_key: str  = "secret123"
    database_url: str = "postgresql+psycopg:///bd2_library_db"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


settings = Settings()# type: ignore