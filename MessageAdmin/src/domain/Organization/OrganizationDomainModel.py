from dataclasses import dataclass
from domain.DomainException import DomainException

@dataclass
class OrganizationDomainModel:
    organization: str  # ID único de la organización
    
    def __post_init__(self):
        """Validaciones del modelo de dominio"""
        if not self.organization:
            raise DomainException("El campo 'organization' es obligatorio.") 