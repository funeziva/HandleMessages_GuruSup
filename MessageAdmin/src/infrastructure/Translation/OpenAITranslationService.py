from openai import OpenAI
from domain.Translation.TranslationServiceInterface import TranslationServiceInterface
from config.Translation_config import OPENAI_API_KEY, OPENAI_MODEL, OPENAI_TIMEOUT
from config.Logger_config import get_logger
from infrastructure.InfrastructureException import InfrastructureException

logger = get_logger(__name__)

class OpenAITranslationService(TranslationServiceInterface):
    def __init__(self):
        if not OPENAI_API_KEY:
            logger.error("No se ha configurado la clave de API de OpenAI")
            raise InfrastructureException("No se ha configurado la clave de API de OpenAI")
        
        self.client = OpenAI(api_key=OPENAI_API_KEY)
    
    async def translate_text(self, text: str, target_language: str = "es") -> str:
        """
        Traduce un texto al idioma de destino utilizando OpenAI API.
        
        Args:
            text: Texto a traducir
            target_language: Código ISO del idioma de destino (por defecto, español)
            
        Returns:
            Texto traducido
        """
        if not text:
            return ""
        
        try:
            # Crear un prompt que indique la traducción deseada
            prompt = f"Traduce el siguiente texto al {target_language}:\n\n{text}"
            
            # Llamar a la API de OpenAI para realizar la traducción
            response = self.client.chat.completions.create(
                model=OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": f"Eres un traductor profesional. Traduce el texto al {target_language} manteniendo el formato original."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1500,
                temperature=0.3
            )
            
            # Extraer y devolver la traducción
            translated_text = response.choices[0].message.content.strip()
            logger.info(f"Texto traducido correctamente a {target_language}")
            return translated_text
            
        except Exception as e:
            logger.error(f"Error al traducir texto: {e}")
            # En caso de error, devolver el texto original
            return text 