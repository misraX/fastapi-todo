from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Todo API"
    debug: bool = True
    database_url: str = ""
    reader_writer_database_url: str = database_url
    model_config = SettingsConfigDict(env_file=".env")


@lru_cache
def get_settings():
    return Settings()


settings = get_settings()
