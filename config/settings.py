"""Settings for the application."""

import os
from pathlib import Path

from dotenv import load_dotenv

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)


class Settings:
    """Class to store the application settings."""

    ENV: str = os.getenv("ENV", "dev")
    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "library-api")
    PROJECT_VERSION: str = os.getenv("PROJECT_VERSION", "1.0.0")
    API_V1_STR: str = "/v1"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "SECRET_KEY")
    if os.getenv("ENV") == "dev":
        _postgres_server = os.getenv("POSTGRES_SERVER_DEV", "localhost")
        _postgres_password = os.getenv("POSTGRES_PASSWORD_DEV", "postgres")
        _postgres_user = os.getenv("POSTGRES_USER_DEV", "postgres")
        _postgres_db = os.getenv("POSTGRES_DB_DEV", "5432")
        _mercado_pago_access_token = os.getenv("MERCADO_PAGO_TEST_ACCESS_TOKEN", "")
        _mercado_pago_secret_key = os.getenv("MERCADO_PAGO_TEST_SECRET_KEY", "")
    else:
        _postgres_server = os.getenv("POSTGRES_SERVER", "localhost")
        _postgres_password = os.getenv("POSTGRES_PASSWORD", "postgres")
        _postgres_user = os.getenv("POSTGRES_USER", "postgres")
        _postgres_db = os.getenv("POSTGRES_DB", "5432")

    POSTGRES_SERVER: str = _postgres_server
    POSTGRES_PASSWORD = _postgres_password
    POSTGRES_USER: str = _postgres_user
    POSTGRES_DB: str = _postgres_db
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", "5432")
    DATABASE_URL: str = f"postgresql+psycopg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))


settings = Settings()
