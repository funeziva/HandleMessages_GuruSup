import grpc
from config.Logger_config import get_logger
from infrastructure.MongoDB.MessageMongoRepository import MessageMongoRepository
from infrastructure.MongoDB.ThreadMongoRepository import ThreadMongoRepository
from infrastructure.MongoDB.OrganizationMongoRepository import OrganizationMongoRepository
from infrastructure.MongoDB.UserMongoRepository import UserMongoRepository
from infrastructure.Translation.OpenAITranslationService import OpenAITranslationService
from infrastructure.GRPC.generated import message_service_pb2, message_service_pb2_grpc
from application.Message.CreateMessageUseCase import CreateMessageUseCase
from application.Thread.FindOrCreateThreadUseCase import FindOrCreateThreadUseCase
from application.User.CreateUserUseCase import CreateUserUseCase
from application.Translation.TranslateTextUseCase import TranslateTextUseCase

logger = get_logger(__name__)

class EmailServicer(message_service_pb2_grpc.EmailServiceServicer):
    def __init__(self):
        # Repositorios
        self.message_repository = MessageMongoRepository()
        self.thread_repository = ThreadMongoRepository()
        self.organization_repository = OrganizationMongoRepository()
        self.user_repository = UserMongoRepository()
        
        # Servicios
        self.translation_service = OpenAITranslationService()
        
        # Casos de uso
        self.translate_text_use_case = TranslateTextUseCase(self.translation_service)
        self.create_user_use_case = CreateUserUseCase(self.user_repository)
        self.find_or_create_thread_use_case = FindOrCreateThreadUseCase(self.thread_repository)
        self.create_message_use_case = CreateMessageUseCase(
            self.message_repository,
            self.translate_text_use_case,
            self.create_user_use_case,
            self.find_or_create_thread_use_case
        )
    
    async def _extract_organization_from_email(self, email: str) -> str:
        """
        Extrae el dominio de la organización a partir de una dirección de correo electrónico.
        
        Args:
            email: Dirección de correo electrónico
            
        Returns:
            Dominio de la organización
        """
        try:
            # Extraer el dominio del correo electrónico
            domain = email.split('@')[1].lower() if '@' in email else email
            return domain
        except Exception as e:
            logger.error(f"Error al extraer el dominio del correo electrónico: {e}")
            return "unknown_organization"
    
    async def SendEmail(self, request, context):
        """
        Implementación del método SendEmail del servicio gRPC.
        
        Args:
            request: Solicitud de correo electrónico desde gRPC
            context: Contexto de la llamada gRPC
            
        Returns:
            Respuesta de correo electrónico gRPC
        """
        try:
            logger.info(f"Recibido email con ID: {request.id}")
            
            # Extraer organización del remitente
            organization = await self._extract_organization_from_email(request.sender)
            
            # Procesar y guardar el mensaje usando el caso de uso
            message = await self.create_message_use_case.execute(
                message_id=request.id,
                sender=request.sender,
                subject=request.subject,
                body=request.body,
                organization=organization,
                recipients=request.recipients
            )
            
            # Devolver respuesta exitosa
            return message_service_pb2.EmailResponse(
                message=f"Email con ID {request.id} procesado correctamente y asignado al hilo {message.thread_id}",
                success=True
            )
        except Exception as e:
            logger.error(f"Error al procesar email: {e}")
            return message_service_pb2.EmailResponse(
                message=f"Error al procesar email: {str(e)}",
                success=False
            ) 