from typing import List, Optional
from config.Logger_config import get_logger
from domain.Message.MessageDomainModel import MessageDomainModel
from domain.Message.MessageRepositoryInterface import MessageRepositoryInterface

logger = get_logger(__name__)

class GetMessageUseCase:
    def __init__(self, message_repository: MessageRepositoryInterface):
        self.message_repository = message_repository
    
    async def get_by_id(self, message_id: str) -> Optional[MessageDomainModel]:
        """
        Obtiene un mensaje por su ID.
        
        Args:
            message_id: ID del mensaje
            
        Returns:
            Modelo de dominio del mensaje, o None si no se encuentra
        """
        try:
            message = await self.message_repository.find_by_id(message_id)
            return message
        except Exception as e:
            logger.error(f"Error al obtener mensaje por ID: {e}")
            raise
    
    async def get_by_organization(self, organization: str) -> List[MessageDomainModel]:
        """
        Obtiene todos los mensajes de una organización.
        
        Args:
            organization: ID de la organización
            
        Returns:
            Lista de modelos de dominio de mensajes
        """
        try:
            messages = await self.message_repository.find_by_organization(organization)
            return messages
        except Exception as e:
            logger.error(f"Error al obtener mensajes por organización: {e}")
            raise 