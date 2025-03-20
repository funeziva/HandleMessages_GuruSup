from abc import ABC, abstractmethod
from typing import List, Optional
from domain.Organization.OrganizationDomainModel import OrganizationDomainModel

class OrganizationRepositoryInterface(ABC):
    @abstractmethod
    async def save(self, organization: OrganizationDomainModel) -> str:
        """
        Guarda una organización en la base de datos.
        
        Args:
            organization: Modelo de dominio de la organización
            
        Returns:
            ID de la organización guardada
        """
        pass
    
    @abstractmethod
    async def find_by_id(self, organization_id: str) -> Optional[OrganizationDomainModel]:
        """
        Busca una organización por su ID.
        
        Args:
            organization_id: ID de la organización a buscar
            
        Returns:
            Modelo de dominio de la organización, o None si no se encuentra
        """
        pass
    
    @abstractmethod
    async def get_all(self) -> List[OrganizationDomainModel]:
        """
        Obtiene todas las organizaciones registradas.
        
        Returns:
            Lista de modelos de dominio de organizaciones
        """
        pass 