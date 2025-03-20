from typing import List, Optional, Dict, Any
from motor.motor_asyncio import AsyncIOMotorDatabase
from domain.Thread.ThreadRepositoryInterface import ThreadRepositoryInterface
from domain.Thread.ThreadDomainModel import ThreadDomainModel
from config.Database_config import get_database
from config.Logger_config import get_logger
from infrastructure.InfrastructureException import InfrastructureException

logger = get_logger(__name__)

class ThreadMongoRepository(ThreadRepositoryInterface):
    def __init__(self):
        self.db = None
        self.collection_name = "cdThread"
    
    async def _get_collection(self):
        if self.db is None:
            self.db = await get_database()
        return self.db[self.collection_name]
    
    def _to_domain_model(self, db_model: Dict[str, Any]) -> ThreadDomainModel:
        """Convierte un documento de MongoDB a un modelo de dominio"""
        if not db_model:
            return None
        
        return ThreadDomainModel(
            FID=db_model["FID"],
            organization=db_model["organization"],
            messages=db_model.get("messages", [])
        )
    
    def _to_db_model(self, domain_model: ThreadDomainModel) -> Dict[str, Any]:
        """Convierte un modelo de dominio a un documento de MongoDB"""
        return {
            "FID": domain_model.FID,
            "organization": domain_model.organization,
            "messages": domain_model.messages
        }
    
    async def save(self, thread: ThreadDomainModel) -> str:
        """
        Guarda un hilo en la base de datos.
        
        Args:
            thread: Modelo de dominio del hilo
            
        Returns:
            ID del hilo guardado
        """
        try:
            collection = await self._get_collection()
            db_model = self._to_db_model(thread)
            
            # Verificar si ya existe un hilo con este FID
            existing_thread = await collection.find_one({"FID": thread.FID})
            if existing_thread:
                # Actualizar el hilo existente
                await collection.update_one(
                    {"FID": thread.FID},
                    {"$set": db_model}
                )
                logger.info(f"Hilo actualizado con FID: {thread.FID}")
            else:
                # Insertar nuevo hilo
                result = await collection.insert_one(db_model)
                logger.info(f"Hilo guardado con FID: {thread.FID}")
            
            return thread.FID
        except Exception as e:
            logger.error(f"Error al guardar hilo: {e}")
            raise InfrastructureException(f"Error al guardar hilo: {e}")
    
    async def find_by_id(self, thread_id: str) -> Optional[ThreadDomainModel]:
        """
        Busca un hilo por su ID.
        
        Args:
            thread_id: ID del hilo a buscar
            
        Returns:
            Modelo de dominio del hilo, o None si no se encuentra
        """
        try:
            collection = await self._get_collection()
            db_model = await collection.find_one({"FID": thread_id})
            if not db_model:
                return None
            
            return self._to_domain_model(db_model)
        except Exception as e:
            logger.error(f"Error al buscar hilo por ID: {e}")
            raise InfrastructureException(f"Error al buscar hilo por ID: {e}")
    
    async def find_by_organization(self, organization: str) -> List[ThreadDomainModel]:
        """
        Busca todos los hilos de una organización.
        
        Args:
            organization: ID de la organización
            
        Returns:
            Lista de modelos de dominio de hilos
        """
        try:
            collection = await self._get_collection()
            cursor = collection.find({"organization": organization})
            threads = []
            
            async for db_model in cursor:
                thread = self._to_domain_model(db_model)
                threads.append(thread)
            
            return threads
        except Exception as e:
            logger.error(f"Error al buscar hilos por organización: {e}")
            raise InfrastructureException(f"Error al buscar hilos por organización: {e}")
    
    async def add_message_to_thread(self, thread_id: str, message_id: str) -> bool:
        """
        Añade un mensaje a un hilo existente.
        
        Args:
            thread_id: ID del hilo
            message_id: ID del mensaje a añadir
            
        Returns:
            True si se añadió correctamente, False en caso contrario
        """
        try:
            collection = await self._get_collection()
            
            # Verificar si el hilo existe
            thread = await collection.find_one({"FID": thread_id})
            if not thread:
                logger.warning(f"No se encontró el hilo con FID: {thread_id}")
                return False
            
            # Verificar si el mensaje ya está en el hilo
            if message_id in thread.get("messages", []):
                logger.info(f"El mensaje {message_id} ya está en el hilo {thread_id}")
                return True
            
            # Añadir el mensaje al hilo
            result = await collection.update_one(
                {"FID": thread_id},
                {"$push": {"messages": message_id}}
            )
            
            if result.modified_count > 0:
                logger.info(f"Mensaje {message_id} añadido al hilo {thread_id}")
                return True
            else:
                logger.warning(f"No se pudo añadir el mensaje {message_id} al hilo {thread_id}")
                return False
                
        except Exception as e:
            logger.error(f"Error al añadir mensaje al hilo: {e}")
            raise InfrastructureException(f"Error al añadir mensaje al hilo: {e}") 