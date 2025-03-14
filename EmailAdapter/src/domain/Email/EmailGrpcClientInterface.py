from domain.Email import EmailDomainModel
from abc import ABC, abstractmethod

class EmailGrpcClientInterface(ABC):
    @abstractmethod
    def send_email_to_message_admin(self, email: EmailDomainModel) -> None:
        """
        Envía la información del email (representado por email_domain_model)
        al microservicio MessageAdmin vía gRPC.
        """
        pass
