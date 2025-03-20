from typing import List, Optional
from config.Logger_config import get_logger
from domain.User.UserDomainModel import UserDomainModel
from domain.User.UserRepositoryInterface import UserRepositoryInterface

logger = get_logger(__name__)

class GetUserUseCase:
    def __init__(self, user_repository: UserRepositoryInterface):
        self.user_repository = user_repository
    
    async def get_by_email(self, email: str) -> Optional[UserDomainModel]:
        """
        Obtiene un usuario por su email.
        
        Args:
            email: Email del usuario
            
        Returns:
            Modelo de dominio del usuario, o None si no se encuentra
        """
        try:
            user = await self.user_repository.find_by_email(email)
            return user
        except Exception as e:
            logger.error(f"Error al obtener usuario por email: {e}")
            raise
    
    async def get_by_organization(self, organization: str) -> List[UserDomainModel]:
        """
        Obtiene todos los usuarios de una organización.
        
        Args:
            organization: ID de la organización
            
        Returns:
            Lista de modelos de dominio de usuarios
        """
        try:
            users = await self.user_repository.find_by_organization(organization)
            return users
        except Exception as e:
            logger.error(f"Error al obtener usuarios por organización: {e}")
            raise
    
    async def get_all(self) -> List[UserDomainModel]:
        """
        Obtiene todos los usuarios registrados.
        
        Returns:
            Lista de modelos de dominio de usuarios
        """
        try:
            users = await self.user_repository.get_all()
            return users
        except Exception as e:
            logger.error(f"Error al obtener todos los usuarios: {e}")
            raise 