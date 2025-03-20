from typing import List, Optional
from config.Logger_config import get_logger
from domain.Thread.ThreadRepositoryInterface import ThreadRepositoryInterface
from domain.Thread.ThreadDomainModel import ThreadDomainModel

logger = get_logger(__name__)

class GetThreadUseCase:
    def __init__(self, repository: ThreadRepositoryInterface):
        self.repository = repository
    
    async def get_by_id(self, thread_id: str) -> Optional[ThreadDomainModel]:
        """
        Obtiene un hilo por su ID.
        
        Args:
            thread_id: ID del hilo
            
        Returns:
            Hilo si existe, None en caso contrario
        """
        try:
            return await self.repository.get_by_id(thread_id)
        except Exception as e:
            logger.error(f"Error al obtener hilo por ID {thread_id}: {e}")
            raise
    
    async def get_by_organization(self, organization: str) -> List[ThreadDomainModel]:
        """
        Obtiene todos los hilos de una organización.
        
        Args:
            organization: Nombre de la organización
            
        Returns:
            Lista de hilos
        """
        try:
            return await self.repository.get_by_organization_id(organization)
        except Exception as e:
            logger.error(f"Error al obtener hilos de la organización {organization}: {e}")
            raise
            
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[ThreadDomainModel]:
        """
        Obtiene todos los hilos.
        
        Returns:
            Lista de hilos
        """
        try:
            return await self.repository.get_all(skip, limit)
        except Exception as e:
            logger.error(f"Error al obtener todos los hilos: {e}")
            raise 