from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    app_name: str
    environment: str
    debug: bool
    mongo_uri: str
    mongo_db_name: str
    jwt_secret_key: str
    jwt_algorithm: str
    jwt_expire_minutes: int
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()

