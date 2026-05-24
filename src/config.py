from pathlib import Path

from pydantic import PostgresDsn, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(Path(__file__).parent.parent / ".env"), env_file_encoding="utf-8"
    )

    DB_NAME: str
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str

    pool_size: int = 10
    max_overflow: int = 20
    pool_recycle: int = 1800
    pool_pre_ping: bool = True
    echo: bool = False

    @computed_field
    @property
    def db_url(self) -> str:
        return str(
            PostgresDsn.build(
                scheme="postgresql+psycopg",
                username=self.DB_USER,
                password=self.DB_PASSWORD,
                host=self.DB_HOST,
                port=self.DB_PORT,
                path=self.DB_NAME,
            )
        )


settings = Settings()
