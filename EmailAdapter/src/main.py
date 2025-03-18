from config.Logger_config import get_logger
from infrastructure.Email.Events.EmailConsumer import EmailConsumer
from infrastructure.Email.GRPC.EmailGrpcClient import EmailGrpcClient
from application.Email.HandleEmailUserCase import HandleEmailUserCase
from config.Settings import settings

def main():

    logger = get_logger(__name__)

    logger.info("[Main] Creating container dependencies...")
    # 1. Instanciar el cliente gRPC (implementación concreta de la interfaz)
    grpc_client = EmailGrpcClient(host=settings.GRPC_HOST, port=settings.GRPC_PORT)
    
    # 2. Crear el caso de uso inyectando el cliente gRPC
    handle_email_event_use_case = HandleEmailUserCase(grpc_client=grpc_client)
    
    # 3. Crear el consumidor Kafka, inyectando el caso de uso
    consumer = EmailConsumer(
        bootstrap_servers=[settings.KAFKA_BOOTSTRAP_SERVERS],
        topic_name=settings.KAFKA_TOPIC,
        group_id=settings.KAFKA_GROUP_ID,
        handle_email_event_use_case=handle_email_event_use_case,
        max_retries=settings.MAX_RETRIES,
        dlq_topic=settings.DLQ_TOPIC
    )
    
    # 4. Iniciar el bucle de consumo (bloqueante)
    consumer.start_consuming()

    logger.info("[Main] Consumer started. Waiting for messages...")

if __name__ == "__main__":
    main()
