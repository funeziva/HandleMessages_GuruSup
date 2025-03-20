from dataclasses import dataclass, field
from typing import List
from domain.DomainException import DomainException

@dataclass
class ThreadDomainModel:
    FID: str  # ID único del hilo
    organization: str  # Organización a la que pertenece el hilo
    messages: List[str] = field(default_factory=list)  # Lista de IDs de mensajes que forman parte del hilo
    
    def __post_init__(self):
        """Validaciones del modelo de dominio"""
        if not self.FID:
            raise DomainException("El campo 'FID' es obligatorio.")
        if not self.organization:
            raise DomainException("El campo 'organization' es obligatorio.")
        if not isinstance(self.messages, list):
            raise DomainException("El campo 'messages' debe ser una lista.") 