from dataclasses import dataclass
from typing import Optional
from domain.DomainException import DomainException

@dataclass
class MessageDomainModel:
    PID: str  # ID único del mensaje
    sender: str  # Remitente del mensaje
    subject: str  # Asunto del mensaje
    body: str  # Cuerpo del mensaje
    organization: str  # Organización a la que pertenece el mensaje
    thread_id: Optional[str] = None  # ID del hilo al que pertenece (puede ser None para mensajes nuevos)
    
    def __post_init__(self):
        """Validaciones del modelo de dominio"""
        if not self.PID:
            raise DomainException("El campo 'PID' es obligatorio.")
        if not self.sender:
            raise DomainException("El campo 'sender' es obligatorio.")
        if not self.subject:
            raise DomainException("El campo 'subject' es obligatorio.")
        if not self.body:
            raise DomainException("El campo 'body' es obligatorio.")
        if not self.organization:
            raise DomainException("El campo 'organization' es obligatorio.") 