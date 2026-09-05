from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "API de Pedidos"
    app_version: str = "1.0.0"

    database_url: str = "postgresql+psycopg://pedidos:pedidos@localhost:5432/pedidos"
    db_echo: bool = False

    db_connect_retries: int = 10
    db_connect_retry_delay: float = 2.0


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
