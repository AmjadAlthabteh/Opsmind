from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings and configuration"""

    # Application
    app_name: str = "AI Incident Commander"
    debug: bool = True
    environment: str = "development"

    # OpenAI
    openai_api_key: str = ""

    # CORS
    cors_origins: str = "*"  # Comma-separated list of allowed origins

    # Rate Limiting
    rate_limit_per_minute: int = 100

    # Vector Database
    vector_db_path: str = "./faiss_index"

    # Observability
    prometheus_port: int = 8001

    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()
