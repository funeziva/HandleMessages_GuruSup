from config.Logger_config import get_logger
from domain.Thread.ThreadRepositoryInterface import ThreadRepositoryInterface
from domain.Message.MessageRepositoryInterface import MessageRepositoryInterface

logger = get_logger(__name__)

class AddMessageToThreadUseCase:
    def __init__(
        self, 
        thread_repository: ThreadRepositoryInterface,
        message_repository: MessageRepositoryInterface
    ):
        self.thread_repository = thread_repository
        self.message_repository = message_repository
    
    async def execute(self, thread_id: str, message_id: str) -> bool:
        """
        Añade un mensaje a un hilo existente.
        
        Args:
            thread_id: ID del hilo
            message_id: ID del mensaje a añadir
            
        Returns:
            True si se añadió correctamente, False en caso contrario
        """
        try:
            # Verificar que el mensaje existe
            message = await self.message_repository.find_by_id(message_id)
            if not message:
                logger.warning(f"No se encontró el mensaje con ID: {message_id}")
                return False
            
            # Verificar que el hilo existe
            thread = await self.thread_repository.find_by_id(thread_id)
            if not thread:
                logger.warning(f"No se encontró el hilo con ID: {thread_id}")
                return False
            
            # Añadir el mensaje al hilo
            result = await self.thread_repository.add_message(thread_id, message_id)
            
            if result:
                # Actualizar el mensaje con el ID del hilo
                message.thread_id = thread_id
                await self.message_repository.save(message)
                logger.info(f"Mensaje {message_id} añadido al hilo {thread_id}")
            else:
                logger.warning(f"No se pudo añadir el mensaje {message_id} al hilo {thread_id}")
            
            return result
            
        except Exception as e:
            logger.error(f"Error al añadir mensaje al hilo: {e}")
            raise 