import json
import time
from kafka import KafkaConsumer, KafkaProducer
from config.Logger_config import get_logger

logger = get_logger(__name__)

class EmailConsumer:
    def __init__(self, bootstrap_servers, topic_name, group_id, handle_email_event_use_case, max_retries=3, dlq_topic="EmailEvents.DLQ"):
        """
        - bootstrap_servers: Lista de servidores Kafka.
        - topic_name: Nombre del topic principal.
        - group_id: Grupo de consumo.
        - handle_email_event_use_case: Instancia del caso de uso de aplicación.
        - max_retries: Número máximo de reintentos antes de enviar a DLQ.
        - dlq_topic: Topic para mensajes fallidos (Dead Letter Queue).
        """
        self.topic_name = topic_name
        self.handle_email_event_use_case = handle_email_event_use_case
        self.max_retries = max_retries
        self.dlq_topic = dlq_topic

        self.consumer = KafkaConsumer(
            topic_name,
            bootstrap_servers=bootstrap_servers,
            group_id=group_id,
            auto_offset_reset='earliest',
            enable_auto_commit=False,  # Commit manual para controlar el reintento
            value_deserializer=lambda m: json.loads(m.decode('utf-8'))
        )

        self.dlq_producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )

    def start_consuming(self):
        logger.info(f"[EmailConsumer] Starting consumer with topic: {self.topic_name}")
        for message in self.consumer:
            self.process_message(message)

    def process_message(self, message):
        retries = 0
        email_data = message.value
        while retries <= self.max_retries:
            try:
                logger.info(f"Proccesing email: {email_data}")
                self.handle_email_event_use_case.execute(email_data)
                self.consumer.commit()
                return
            except Exception as e:
                retries += 1
                logger.error(f"[EmailConsumer] Error processing email (retry {retries}/{self.max_retries}): {e}")
                if retries > self.max_retries:
                    self.handle_exception(email_data, e)
                    self.consumer.commit()  
                    return
                else:
                    time.sleep(2 ** retries)

    def handle_exception(self, email_data, exception):
        logger.error(f"[EmailConsumer] Max retries over, sending email to DLQ")
        try:
            self.dlq_producer.send(self.dlq_topic, email_data)
            self.dlq_producer.flush()
        except Exception as ex:
            logger.error(f"[EmailConsumer] Error sending to DLQ: {ex}")
