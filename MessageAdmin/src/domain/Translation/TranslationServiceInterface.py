from abc import ABC, abstractmethod

class TranslationServiceInterface(ABC):
    @abstractmethod
    async def translate_text(self, text: str, target_language: str = "es") -> str:
        """
        Traduce un texto al idioma de destino.
        
        Args:
            text: Texto a traducir
            target_language: Código ISO del idioma de destino (por defecto, español)
            
        Returns:
            Texto traducido
        """
        pass 