from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    GRPC_HOST: str = "localhost"
    GRPC_PORT: int = 50051
    KAFKA_BOOTSTRAP_SERVERS: str = "localhost:9092"
    KAFKA_TOPIC: str = "EmailEvent"
    KAFKA_GROUP_ID: str = "email_adapter_group"
    MAX_RETRIES: int = 3
    DLQ_TOPIC: str = "EmailEvent.DLQ"

    class Config:
        env_file = ".env"  # Indica que lea las variables de este archivo

settings = Settings()
