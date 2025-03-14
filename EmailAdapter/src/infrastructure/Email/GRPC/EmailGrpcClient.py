# src/infrastructure/GRPC/EmailGrpcClient.py

import grpc
from infrastructure.Email.GRPC.generated import email_pb2_grpc, email_pb2  # Importamos los stubs generados
from domain.Email.EmailGrpcClientInterface import EmailGrpcClientInterface
from domain.Email.EmailDomainModel import EmailDomainModel

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
        try:
            # Llamada remota
            response = self.stub.SendEmail(email_pb2.EmailRequest(
                id=email.id,
                subject=email.subject,
                body=email.body,
                sender=email.sender,
                recipients=email.recipients
            ))
            print(f"[EmailGrpcClient] Respuesta de MessageAdmin: {response.message}")
        except Exception as e:
            print(f"[EmailGrpcClient] Error al enviar el email: {e}")
        
