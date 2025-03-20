from abc import ABC, abstractmethod
from typing import List, Optional
from domain.Message.MessageDomainModel import MessageDomainModel

class MessageRepositoryInterface(ABC):
    @abstractmethod
    async def save(self, message: MessageDomainModel) -> str:
        """
        Guarda un mensaje en la base de datos.
        
        Args:
            message: Modelo de dominio del mensaje
            
        Returns:
            ID del mensaje guardado
        """
        pass
    
    @abstractmethod
    async def find_by_id(self, message_id: str) -> Optional[MessageDomainModel]:
        """
        Busca un mensaje por su ID.
        
        Args:
            message_id: ID del mensaje a buscar
            
        Returns:
            Modelo de dominio del mensaje, o None si no se encuentra
        """
        pass
    
    @abstractmethod
    async def find_by_organization(self, organization: str) -> List[MessageDomainModel]:
        """
        Busca todos los mensajes de una organización.
        
        Args:
            organization: ID de la organización
            
        Returns:
            Lista de modelos de dominio de mensajes
        """
        pass 