from domain.Email.EmailDomainModel import EmailDomainModel
from abc import ABC, abstractmethod

class EmailAzureBlobRepositoryInterface(ABC):
    @abstractmethod
    async def saveEmail(self, message: EmailDomainModel) -> None:
        """
        Guarda el mensaje en Azure Blob Storage de forma asíncrona.
        """
        pass
