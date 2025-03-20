from abc import ABC, abstractmethod
from typing import List, Optional
from domain.User.UserDomainModel import UserDomainModel

class UserRepositoryInterface(ABC):
    @abstractmethod
    async def save(self, user: UserDomainModel) -> str:
        """
        Guarda un usuario en la base de datos.
        
        Args:
            user: Modelo de dominio del usuario
            
        Returns:
            Email del usuario guardado
        """
        pass
    
    @abstractmethod
    async def find_by_email(self, email: str) -> Optional[UserDomainModel]:
        """
        Busca un usuario por su email.
        
        Args:
            email: Email del usuario a buscar
            
        Returns:
            Modelo de dominio del usuario, o None si no se encuentra
        """
        pass
    
    @abstractmethod
    async def find_by_organization(self, organization: str) -> List[UserDomainModel]:
        """
        Busca todos los usuarios de una organización.
        
        Args:
            organization: ID de la organización
            
        Returns:
            Lista de modelos de dominio de usuarios
        """
        pass
    
    @abstractmethod
    async def get_all(self) -> List[UserDomainModel]:
        """
        Obtiene todos los usuarios registrados.
        
        Returns:
            Lista de modelos de dominio de usuarios
        """
        pass 

    @abstractmethod
    async def find_by_id(self, user_id: str) -> Optional[UserDomainModel]:
        """
        Busca un usuario por su ID.
        
        Args:
            user_id: ID del usuario a buscar
            
        Returns:
            Modelo de dominio del usuario, o None si no se encuentra
        """
        pass
