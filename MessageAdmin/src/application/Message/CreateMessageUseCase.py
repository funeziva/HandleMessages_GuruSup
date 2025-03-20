from config.Logger_config import get_logger
from domain.Message.MessageDomainModel import MessageDomainModel
from domain.Message.MessageRepositoryInterface import MessageRepositoryInterface
from application.Translation.TranslateTextUseCase import TranslateTextUseCase
from application.User.CreateUserUseCase import CreateUserUseCase
from application.Thread.FindOrCreateThreadUseCase import FindOrCreateThreadUseCase

logger = get_logger(__name__)

class CreateMessageUseCase:
    def __init__(
        self, 
        message_repository: MessageRepositoryInterface,
        translate_use_case: TranslateTextUseCase,
        create_user_use_case: CreateUserUseCase,
        find_or_create_thread_use_case: FindOrCreateThreadUseCase
    ):
        self.message_repository = message_repository
        self.translate_use_case = translate_use_case
        self.create_user_use_case = create_user_use_case
        self.find_or_create_thread_use_case = find_or_create_thread_use_case
    
    async def execute(
        self,
        message_id: str,
        sender: str,
        subject: str,
        body: str,
        organization: str,
        recipients: list = None
    ) -> MessageDomainModel:
        """
        Crea un nuevo mensaje con traducciones y lo relaciona con usuarios y hilos.
        
        Args:
            message_id: ID único del mensaje
            sender: Remitente del mensaje
            subject: Asunto del mensaje
            body: Cuerpo del mensaje
            organization: Organización a la que pertenece el mensaje
            recipients: Lista de destinatarios
            
        Returns:
            Modelo de dominio del mensaje creado
        """
        try:
            # Guardar o actualizar el remitente como usuario
            await self.create_user_use_case.execute(
                email=sender,
                organization=organization
            )
            
            # Guardar o actualizar los destinatarios como usuarios
            if recipients:
                for recipient in recipients:
                    await self.create_user_use_case.execute(
                        email=recipient,
                        organization=organization
                    )
            
            # Traducir el asunto y el cuerpo del mensaje
            translated_subject = await self.translate_use_case.execute(subject)
            translated_body = await self.translate_use_case.execute(body)
            
            # Crear el modelo de dominio del mensaje
            message = MessageDomainModel(
                PID=message_id,
                sender=sender,
                subject=translated_subject,
                body=translated_body,
                organization=organization
            )
            
            # Guardar el mensaje en la base de datos
            await self.message_repository.save(message)
            
            # Determinar si es parte de un hilo existente o crear uno nuevo
            thread_id = await self.find_or_create_thread_use_case.execute(message)
            
            # Actualizar el mensaje con el ID del hilo
            message.thread_id = thread_id
            await self.message_repository.save(message)
            
            logger.info(f"Mensaje creado con ID: {message_id}")
            return message
            
        except Exception as e:
            logger.error(f"Error al crear mensaje: {e}")
            raise 