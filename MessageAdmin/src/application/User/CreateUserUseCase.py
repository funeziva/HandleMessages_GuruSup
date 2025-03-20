from typing import Optional
from config.Logger_config import get_logger
from domain.User.UserDomainModel import UserDomainModel
from domain.User.UserRepositoryInterface import UserRepositoryInterface

logger = get_logger(__name__)

class CreateUserUseCase:
    def __init__(self, user_repository: UserRepositoryInterface):
        self.user_repository = user_repository
    
    async def execute(
        self,
        email: str,
        name: Optional[str] = None,
        organization: Optional[str] = None
    ) -> UserDomainModel:
        """
        Crea un nuevo usuario o actualiza uno existente.
        
        Args:
            email: Email del usuario
            name: Nombre del usuario (opcional)
            organization: Organización a la que pertenece (opcional)
            
        Returns:
            Modelo de dominio del usuario creado o actualizado
        """
        try:
            # Verificar si el usuario ya existe
            existing_user = await self.user_repository.find_by_email(email)
            
            if existing_user:
                # Actualizar datos si es necesario
                update_needed = False
                
                if name and existing_user.name != name:
                    existing_user.name = name
                    update_needed = True
                
                if organization and existing_user.organization != organization:
                    existing_user.organization = organization
                    update_needed = True
                
                if update_needed:
                    await self.user_repository.save(existing_user)
                    logger.info(f"Usuario actualizado: {email}")
                
                return existing_user
            
            # Crear un nuevo usuario
            user = UserDomainModel(
                email=email,
                name=name,
                organization=organization
            )
            
            await self.user_repository.save(user)
            logger.info(f"Nuevo usuario creado: {email}")
            
            return user
            
        except Exception as e:
            logger.error(f"Error al crear usuario: {e}")
            raise 