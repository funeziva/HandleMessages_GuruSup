from dataclasses import dataclass
from typing import Optional
from domain.DomainException import DomainException

@dataclass
class UserDomainModel:
    email: str  # Email del usuario (identificador único)
    name: Optional[str] = None  # Nombre del usuario
    organization: Optional[str] = None  # Organización a la que pertenece
    
    def __post_init__(self):
        """Validaciones del modelo de dominio"""
        if not self.email:
            raise DomainException("El campo 'email' es obligatorio.") 