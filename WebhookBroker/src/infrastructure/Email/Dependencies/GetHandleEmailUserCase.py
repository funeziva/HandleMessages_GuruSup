from functools import lru_cache
from application.Email.HandleEmailUserCase import HandleEmailUserCase
from infrastructure.Email.Azure.EmailAzureBlobRepository import EmailAzureBlobRepository
from infrastructure.Email.Events.EmailEventPublisher import EmailEventPublisher
from config.Settings import settings

@lru_cache()
def get_HandleEmailUserCase() -> HandleEmailUserCase:
    """
    Crea la instancia de HandleEmailUserCase con las dependencias concretas
    en la capa de infraestructura, utilizando las variables de entorno.
    """
    # Repositorio para guardar en Azure Blob (usando conexión y contenedor reales)
    azure_blob_service = EmailAzureBlobRepository(
        connection_string=settings.AZURE_CONNECTION_STRING,
        container_name=settings.CONTAINER_NAME
    )
    
    # Publicador de eventos en Kafka, con parámetros de reintentos configurados
    kafka_publisher = EmailEventPublisher(
        bootstrap_servers=[settings.KAFKA_BOOTSTRAP_SERVERS],
        topic_name=settings.KAFKA_TOPIC,
        max_retries=settings.MAX_RETRIES,
        retry_backoff=settings.RETRY_BACKOFF
    )
    
    # Inyectamos las dependencias en el caso de uso
    return HandleEmailUserCase(azure_blob_service, kafka_publisher)
