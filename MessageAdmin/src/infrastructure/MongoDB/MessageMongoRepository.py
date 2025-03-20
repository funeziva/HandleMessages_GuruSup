from typing import List, Optional, Dict, Any
from motor.motor_asyncio import AsyncIOMotorDatabase
from domain.Message.MessageRepositoryInterface import MessageRepositoryInterface
from domain.Message.MessageDomainModel import MessageDomainModel
from config.Database_config import get_database
from config.Logger_config import get_logger
from infrastructure.InfrastructureException import InfrastructureException

logger = get_logger(__name__)

class MessageMongoRepository(MessageRepositoryInterface):
    def __init__(self):
        self.db = None
        self.collection_name = "cdMessages"
    
    async def _get_collection(self):
        if self.db is None:
            self.db = await get_database()
        return self.db[self.collection_name]
    
    def _to_domain_model(self, db_model: Dict[str, Any]) -> MessageDomainModel:
        """Convierte un documento de MongoDB a un modelo de dominio"""
        if not db_model:
            return None
        
        return MessageDomainModel(
            PID=db_model["PID"],
            sender=db_model["sender"],
            subject=db_model["subject"],
            body=db_model["body"],
            organization=db_model["organization"],
            thread_id=db_model.get("thread_id")
        )
    
    def _to_db_model(self, domain_model: MessageDomainModel) -> Dict[str, Any]:
        """Convierte un modelo de dominio a un documento de MongoDB"""
        db_model = {
            "PID": domain_model.PID,
            "sender": domain_model.sender,
            "subject": domain_model.subject,
            "body": domain_model.body,
            "organization": domain_model.organization
        }
        
        if domain_model.thread_id:
            db_model["thread_id"] = domain_model.thread_id
        
        return db_model
    
    async def save(self, message: MessageDomainModel) -> str:
        """
        Guarda un mensaje en la base de datos.
        
        Args:
            message: Modelo de dominio del mensaje
            
        Returns:
            ID del mensaje guardado
        """
        try:
            collection = await self._get_collection()
            db_model = self._to_db_model(message)
            
            # Verificar si ya existe un mensaje con este PID
            existing_message = await collection.find_one({"PID": message.PID})
            if existing_message:
                # Actualizar el mensaje existente
                await collection.update_one(
                    {"PID": message.PID},
                    {"$set": db_model}
                )
                logger.info(f"Mensaje actualizado con PID: {message.PID}")
            else:
                # Insertar nuevo mensaje
                result = await collection.insert_one(db_model)
                logger.info(f"Mensaje guardado con PID: {message.PID}")
            
            return message.PID
        except Exception as e:
            logger.error(f"Error al guardar mensaje: {e}")
            raise InfrastructureException(f"Error al guardar mensaje: {e}")
    
    async def find_by_id(self, message_id: str) -> Optional[MessageDomainModel]:
        """
        Busca un mensaje por su ID.
        
        Args:
            message_id: ID del mensaje a buscar
            
        Returns:
            Modelo de dominio del mensaje, o None si no se encuentra
        """
        try:
            collection = await self._get_collection()
            db_model = await collection.find_one({"PID": message_id})
            if not db_model:
                return None
            
            return self._to_domain_model(db_model)
        except Exception as e:
            logger.error(f"Error al buscar mensaje por ID: {e}")
            raise InfrastructureException(f"Error al buscar mensaje por ID: {e}")
    
    async def find_by_organization(self, organization: str) -> List[MessageDomainModel]:
        """
        Busca todos los mensajes de una organización.
        
        Args:
            organization: ID de la organización
            
        Returns:
            Lista de modelos de dominio de mensajes
        """
        try:
            collection = await self._get_collection()
            cursor = collection.find({"organization": organization})
            messages = []
            
            async for db_model in cursor:
                message = self._to_domain_model(db_model)
                messages.append(message)
            
            return messages
        except Exception as e:
            logger.error(f"Error al buscar mensajes por organización: {e}")
            raise InfrastructureException(f"Error al buscar mensajes por organización: {e}") 