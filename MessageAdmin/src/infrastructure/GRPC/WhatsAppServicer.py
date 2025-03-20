import grpc
from config.Logger_config import get_logger
from infrastructure.MongoDB.MessageMongoRepository import MessageMongoRepository
from infrastructure.MongoDB.ThreadMongoRepository import ThreadMongoRepository
from infrastructure.MongoDB.UserMongoRepository import UserMongoRepository
from infrastructure.Translation.OpenAITranslationService import OpenAITranslationService
from infrastructure.GRPC.generated import message_service_pb2, message_service_pb2_grpc
from application.Message.CreateMessageUseCase import CreateMessageUseCase
from application.Thread.FindOrCreateThreadUseCase import FindOrCreateThreadUseCase
from application.User.CreateUserUseCase import CreateUserUseCase
from application.Translation.TranslateTextUseCase import TranslateTextUseCase

logger = get_logger(__name__)

class WhatsAppServicer(message_service_pb2_grpc.WhatsAppServiceServicer):
    def __init__(self):
        # Repositorios
        self.message_repository = MessageMongoRepository()
        self.thread_repository = ThreadMongoRepository()
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
    
    async def _extract_organization_from_number(self, phone_number: str) -> str:
        """
        Extrae el identificador de organización a partir de un número de teléfono.
        
        Args:
            phone_number: Número de teléfono
            
        Returns:
            Identificador de la organización
        """
        try:
            # Extraer primeros dígitos del número (código de país)
            if phone_number.startswith('+'):
                country_code = phone_number[1:3]  # Ejemplo: +34 -> 34
            else:
                country_code = phone_number[:2]  # Fallback
                
            return f"whatsapp_org_{country_code}"
        except Exception as e:
            logger.error(f"Error al extraer la organización del número de teléfono: {e}")
            return "unknown_whatsapp_organization"
    
    async def SendWhatsApp(self, request, context):
        """
        Implementación del método SendWhatsApp del servicio gRPC.
        
        Args:
            request: Solicitud de WhatsApp desde gRPC
            context: Contexto de la llamada gRPC
            
        Returns:
            Respuesta de WhatsApp gRPC
        """
        try:
            logger.info(f"Recibido mensaje de WhatsApp con ID: {request.id}")
            
            # Extraer organización del número de teléfono
            organization = await self._extract_organization_from_number(request.sender)
            
            # Crear un "asunto" a partir del inicio del mensaje
            subject = request.body[:30] + "..." if len(request.body) > 30 else request.body
            
            # Procesar y guardar el mensaje usando el caso de uso
            message = await self.create_message_use_case.execute(
                message_id=request.id,
                sender=request.sender,
                subject=subject,
                body=request.body,
                organization=organization,
                recipients=[request.recipient]
            )
            
            # Devolver respuesta exitosa
            return message_service_pb2.WhatsAppResponse(
                message=f"Mensaje de WhatsApp con ID {request.id} procesado correctamente y asignado al hilo {message.thread_id}",
                success=True
            )
        except Exception as e:
            logger.error(f"Error al procesar mensaje de WhatsApp: {e}")
            return message_service_pb2.WhatsAppResponse(
                message=f"Error al procesar mensaje de WhatsApp: {str(e)}",
                success=False
            ) 