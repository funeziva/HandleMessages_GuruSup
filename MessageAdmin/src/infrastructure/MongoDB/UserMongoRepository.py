from typing import List, Optional, Dict, Any
from domain.User.UserRepositoryInterface import UserRepositoryInterface
from domain.User.UserDomainModel import UserDomainModel
from config.Database_config import get_database
from config.Logger_config import get_logger
from infrastructure.InfrastructureException import InfrastructureException

logger = get_logger(__name__)

class UserMongoRepository(UserRepositoryInterface):
    def __init__(self, db=None):
        self.db = db
        self.collection_name = "cdUsers"
    
    async def _get_collection(self):
        if self.db is None:
            self.db = await get_database()
        return self.db[self.collection_name]
    
    def _to_domain_model(self, db_model: Dict[str, Any]) -> UserDomainModel:
        """Convierte un documento de MongoDB a un modelo de dominio"""
        if not db_model:
            return None
        
        return UserDomainModel(
            email=db_model["email"],
            name=db_model.get("name"),
            organization=db_model.get("organization")
        )
    
    def _to_db_model(self, domain_model: UserDomainModel) -> Dict[str, Any]:
        """Convierte un modelo de dominio a un documento de MongoDB"""
        db_model = {
            "email": domain_model.email
        }
        
        if domain_model.name:
            db_model["name"] = domain_model.name
        
        if domain_model.organization:
            db_model["organization"] = domain_model.organization
        
        return db_model
    
    async def save(self, user: UserDomainModel) -> str:
        """
        Guarda un usuario en la base de datos.
        
        Args:
            user: Modelo de dominio del usuario
            
        Returns:
            Email del usuario guardado
        """
        try:
            collection = await self._get_collection()
            db_model = self._to_db_model(user)
            
            # Verificar si ya existe un usuario con este email
            existing_user = await collection.find_one({"email": user.email})
            if existing_user:
                # Actualizar el usuario existente
                await collection.update_one(
                    {"email": user.email},
                    {"$set": db_model}
                )
                logger.info(f"Usuario actualizado con email: {user.email}")
            else:
                # Insertar nuevo usuario
                result = await collection.insert_one(db_model)
                logger.info(f"Usuario guardado con email: {user.email}")
            
            return user.email
        except Exception as e:
            logger.error(f"Error al guardar usuario: {e}")
            raise InfrastructureException(f"Error al guardar usuario: {e}")
    
    async def find_by_email(self, email: str) -> Optional[UserDomainModel]:
        """
        Busca un usuario por su email.
        
        Args:
            email: Email del usuario a buscar
            
        Returns:
            Modelo de dominio del usuario, o None si no se encuentra
        """
        try:
            collection = await self._get_collection()
            db_model = await collection.find_one({"email": email})
            if not db_model:
                return None
            
            return self._to_domain_model(db_model)
        except Exception as e:
            logger.error(f"Error al buscar usuario por email: {e}")
            raise InfrastructureException(f"Error al buscar usuario por email: {e}")
    
    async def find_by_organization(self, organization: str) -> List[UserDomainModel]:
        """
        Busca todos los usuarios de una organización.
        Si organization es None, trae todos los usuarios.
        
        Args:
            organization: ID de la organización, o None para traer todos
            
        Returns:
            Lista de modelos de dominio de usuarios
        """
        try:
            collection = await self._get_collection()
            filter_query = {} if organization is None else {"organization": organization}
            cursor = collection.find(filter_query)
            users = []
            
            async for db_model in cursor:
                user = self._to_domain_model(db_model)
                users.append(user)
            
            return users
        except Exception as e:
            logger.error(f"Error al buscar usuarios por organización: {e}")
            raise InfrastructureException(f"Error al buscar usuarios por organización: {e}")
    
    async def get_all(self) -> List[UserDomainModel]:
        """
        Obtiene todos los usuarios registrados.
        
        Returns:
            Lista de modelos de dominio de usuarios
        """
        return await self.find_by_organization(None)
    
    async def find_by_id(self, user_id: str) -> Optional[UserDomainModel]:
        """
        Busca un usuario por su ID (que es el email en este caso).
        
        Args:
            user_id: Email del usuario a buscar
            
        Returns:
            Modelo de dominio del usuario, o None si no se encuentra
        """
        try:
            collection = await self._get_collection()
            db_model = await collection.find_one({"email": user_id})
            if not db_model:
                return None
            
            return self._to_domain_model(db_model)
        except Exception as e:
            logger.error(f"Error al buscar usuario por ID: {e}")
            raise InfrastructureException(f"Error al buscar usuario por ID: {e}")
