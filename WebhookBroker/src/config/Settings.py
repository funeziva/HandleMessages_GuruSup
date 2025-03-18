from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    AZURE_CONNECTION_STRING: str
    CONTAINER_NAME: str
    KAFKA_BOOTSTRAP_SERVERS: str
    KAFKA_TOPIC: str
    MAX_RETRIES: int = 3
    RETRY_BACKOFF: float = 2.0

    class Config:
        env_file = ".env"  # Indica que lea las variables de este archivo

settings = Settings()
