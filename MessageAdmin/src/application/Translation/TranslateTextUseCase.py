from config.Logger_config import get_logger
from domain.Translation.TranslationServiceInterface import TranslationServiceInterface

logger = get_logger(__name__)

class TranslateTextUseCase:
    def __init__(self, translation_service: TranslationServiceInterface):
        self.translation_service = translation_service
    
    async def execute(self, text: str, target_language: str = "es") -> str:
        """
        Traduce un texto al idioma de destino.
        
        Args:
            text: Texto a traducir
            target_language: Código ISO del idioma de destino (por defecto, español)
            
        Returns:
            Texto traducido
        """
        try:
            if not text:
                return ""
                
            translated_text = await self.translation_service.translate_text(text, target_language)
            return translated_text
        except Exception as e:
            logger.error(f"Error al traducir texto: {e}")
            # En caso de error, devolver el texto original
            return text 