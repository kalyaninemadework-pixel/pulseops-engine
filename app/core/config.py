import os
from typing import List

try:
    from pydantic_settings import BaseSettings, SettingsConfigDict
    class Settings(BaseSettings):
        PROJECT_NAME: str = os.getenv("PROJECT_NAME", "PulseOps Microservice Engine")
        VERSION: str = "1.0.0"
        API_V1_STR: str = os.getenv("API_V1_STR", "/api/v1")
        SECRET_KEY: str = os.getenv("SECRET_KEY", "pulseops_super_secret_jwt_key_for_development_replace_in_prod")
        ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
        ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "120"))
        DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./pulseops.db")
        REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
        CELERY_BROKER_URL: str = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
        CELERY_RESULT_BACKEND: str = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")
        BACKEND_CORS_ORIGINS: List[str] = ["*"]
        model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")
    settings = Settings()
except Exception:
    class FallbackSettings:
        PROJECT_NAME: str = os.getenv("PROJECT_NAME", "PulseOps Microservice Engine")
        VERSION: str = "1.0.0"
        API_V1_STR: str = os.getenv("API_V1_STR", "/api/v1")
        SECRET_KEY: str = os.getenv("SECRET_KEY", "pulseops_super_secret_jwt_key_for_development_replace_in_prod")
        ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
        ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "120"))
        DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./pulseops.db")
        REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
        CELERY_BROKER_URL: str = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
        CELERY_RESULT_BACKEND: str = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")
        BACKEND_CORS_ORIGINS: List[str] = ["*"]
    settings = FallbackSettings()
