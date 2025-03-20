from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Configuración de gRPC
    GRPC_HOST: str = "0.0.0.0"
    GRPC_PORT: int = 50051
    
    # Configuración de MongoDB
    MONGODB_URI: str = "mongodb://localhost:27017"
    MONGODB_DB: str = "message_admin"
    MONGODB_MIN_POOL_SIZE: int = 10
    MONGODB_MAX_POOL_SIZE: int = 100
    MONGODB_SERVER_SELECTION_TIMEOUT_MS: int = 5000
    MONGODB_CONNECT_TIMEOUT_MS: int = 10000
    MONGODB_SOCKET_TIMEOUT_MS: int = 45000
    MONGODB_RETRY_WRITES: bool = True
    
    # Configuración de OpenAI
    OPENAI_API_KEY: str
    OPENAI_MODEL: str = "gpt-3.5-turbo"
    OPENAI_TIMEOUT: int = 30
    
    # Configuración de API
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    API_WORKERS: int = 4
    API_TIMEOUT: int = 60
    
    class Config:
        env_file = ".env"  # Indica que lea las variables de este archivo
        case_sensitive = True  # Las variables son sensibles a mayúsculas/minúsculas

settings = Settings() 