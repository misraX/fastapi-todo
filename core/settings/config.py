import os
from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Todo API"
    debug: bool = True
    database_url: str = ""
    reader_writer_database_url: str = database_url
    model_config = SettingsConfigDict(env_file=".env")
    base_dir: Path = Path(__file__).parent.parent.parent
    app_dir: Path = os.path.join(base_dir, "app")
    secret_key: str = ""


@lru_cache
def get_settings():
    return Settings()


settings = get_settings()
