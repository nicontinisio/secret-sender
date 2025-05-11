import os

class Settings:
    REDIS_HOST: str = os.getenv("REDIS_HOST", "redis")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", 6379))
    REDIS_PASSWORD: str = os.getenv("REDIS_PASSWORD", "")
    MAX_UPLOAD_MB: int = int(os.getenv("MAX_UPLOAD_MB", 10))
    MAX_UPLOAD_BYTES: int = MAX_UPLOAD_MB * 1024 * 1024

settings = Settings()