import uuid
from config.Logger_config import get_logger
from domain.Message.MessageDomainModel import MessageDomainModel
from domain.Thread.ThreadDomainModel import ThreadDomainModel
from domain.Thread.ThreadRepositoryInterface import ThreadRepositoryInterface

logger = get_logger(__name__)

class FindOrCreateThreadUseCase:
    def __init__(self, thread_repository: ThreadRepositoryInterface):
        self.thread_repository = thread_repository
    
    async def execute(self, message: MessageDomainModel) -> str:
        """
        Busca un hilo existente para el mensaje o crea uno nuevo.
        
        Args:
            message: Modelo de dominio del mensaje
            
        Returns:
            ID del hilo
        """
        try:
            # Analizar el asunto para determinar si es una respuesta
            subject = message.subject.lower()
            is_reply = "re:" in subject or "fw:" in subject or "fwd:" in subject
            
            if is_reply:
                # Buscar hilos existentes por organización
                threads = await self.thread_repository.find_by_organization(message.organization)
                
                # Lógica simple: si hay hilos, añadir el mensaje al último
                if threads:
                    thread = threads[-1]
                    await self.thread_repository.add_message_to_thread(thread.FID, message.PID)
                    logger.info(f"Mensaje {message.PID} añadido al hilo existente {thread.FID}")
                    return thread.FID
            
            # Si no es una respuesta o no se encontró un hilo adecuado, crear uno nuevo
            thread_id = f"thread_{uuid.uuid4().hex}"
            thread = ThreadDomainModel(
                FID=thread_id,
                organization=message.organization,
                messages=[message.PID]
            )
            await self.thread_repository.save(thread)
            logger.info(f"Nuevo hilo creado con ID: {thread_id}")
            
            return thread_id
            
        except Exception as e:
            logger.error(f"Error al buscar o crear hilo: {e}")
            raise 