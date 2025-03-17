from abc import ABC, abstractmethod
from domain.Email import EmailDomainModel

class EmailEventPublisherInterface(ABC):
    @abstractmethod
    def publish_email_event(self, email: EmailDomainModel) -> None:
        """
        Publica un evento con la información del email.
        """
        pass