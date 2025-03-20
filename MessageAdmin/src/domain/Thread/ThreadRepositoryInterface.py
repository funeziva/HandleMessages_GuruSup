from abc import ABC, abstractmethod
from typing import List, Optional
from domain.Thread.ThreadDomainModel import ThreadDomainModel

class ThreadRepositoryInterface(ABC):
    @abstractmethod
    async def save(self, thread: ThreadDomainModel) -> str:
        """
        Guarda un hilo en la base de datos.
        
        Args:
            thread: Modelo de dominio del hilo
            
        Returns:
            ID del hilo guardado
        """
        pass
    
    @abstractmethod
    async def find_by_id(self, thread_id: str) -> Optional[ThreadDomainModel]:
        """
        Busca un hilo por su ID.
        
        Args:
            thread_id: ID del hilo a buscar
            
        Returns:
            Modelo de dominio del hilo, o None si no se encuentra
        """
        pass
    
    @abstractmethod
    async def find_by_organization(self, organization: str) -> List[ThreadDomainModel]:
        """
        Busca todos los hilos de una organización.
        
        Args:
            organization: ID de la organización
            
        Returns:
            Lista de modelos de dominio de hilos
        """
        pass
    
    @abstractmethod
    async def add_message_to_thread(self, thread_id: str, message_id: str) -> bool:
        """
        Añade un mensaje a un hilo existente.
        
        Args:
            thread_id: ID del hilo
            message_id: ID del mensaje a añadir
            
        Returns:
            True si se añadió correctamente, False en caso contrario
        """
        pass 