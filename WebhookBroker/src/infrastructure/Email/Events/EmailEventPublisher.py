import json
import time
from kafka import KafkaProducer
from config.Logger_config import get_logger
from domain.Email.EmailEventPublisherInterface import EmailEventPublisherInterface
from domain.Email.EmailDomainModel import EmailDomainModel
from infrastructure.InfrastructureException import InfrastructureException

class EmailEventPublisher(EmailEventPublisherInterface):
    def __init__(self, bootstrap_servers: list, topic_name: str, max_retries: int = 3, retry_backoff: float = 2.0):
        self.bootstrap_servers = bootstrap_servers
        self.topic_name = topic_name
        self.max_retries = max_retries
        self.retry_backoff = retry_backoff
        self.producer = KafkaProducer(
            bootstrap_servers=self.bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        self.logger = get_logger(__name__)

    def publish_email_event(self, email: EmailDomainModel) -> None:
        """
        Publica el evento (representado por EmailDomainModel) en un topic de Kafka.
        Se implementa manejo de errores y reintentos en caso de fallo.
        """
        email_data = email.dict()  # o vars(email)
        attempt = 0

        while attempt < self.max_retries:
            try:
                future = self.producer.send(self.topic_name, email_data)
                # Esperamos confirmación (lanza excepción en caso de error)
                future.get(timeout=5)
                self.logger.info(f"[KafkaEmailEventPublisher] Evento publicado en Kafka → {self.topic_name}: {email_data}")
                return
            except Exception as e:
                attempt += 1
                self.logger.error(f"Error publicando evento en Kafka (intento {attempt}/{self.max_retries}): {e}")
                if attempt >= self.max_retries:
                    raise InfrastructureException(f"Error al publicar evento en Kafka después de {self.max_retries} intentos", e)
                else:
                    time.sleep(self.retry_backoff)
