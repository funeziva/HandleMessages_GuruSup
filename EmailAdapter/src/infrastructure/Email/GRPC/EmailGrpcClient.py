# src/infrastructure/GRPC/EmailGrpcClient.py

import grpc
from infrastructure.Email.GRPC.generated import email_pb2_grpc, email_pb2  # Importamos los stubs generados
from domain.Email.EmailGrpcClientInterface import EmailGrpcClientInterface
from domain.Email.EmailDomainModel import EmailDomainModel
from config.Logger_config import get_logger

logger = get_logger(__name__)

class EmailGrpcClient(EmailGrpcClientInterface):
    def __init__(self, host="localhost", port=50051):
        # Crear canal gRPC apuntando al microservicio MessageAdmin
        self.channel = grpc.insecure_channel(f"{host}:{port}")
        # Instanciar el stub del servicio EmailService
        self.stub = email_pb2_grpc.EmailServiceStub(self.channel)

    def send_email_to_message_admin(self, email: EmailDomainModel) -> None:
        """
        Serializa el EmailDomainModel en un EmailRequest proto y llama al método remoto SendEmail.
        """
        
        # Llamada remota
        response = self.stub.SendEmail(email_pb2.EmailRequest(
            id=email.id,
            subject=email.subject,
            body=email.text,
            sender=email.sender,
            recipients=email.recipients
        ))
        
        # Comprobar si la solicitud fue exitosa
        if response.success:
            logger.info(f"[EmailGrpcClient] Respuesta exitosa de MessageAdmin: {response.message}")
        else:
            logger.error(f"[EmailGrpcClient] Error en MessageAdmin: {response.message}")
        
