from typing import List, Optional, Dict, Any
from motor.motor_asyncio import AsyncIOMotorDatabase
from domain.Organization.OrganizationRepositoryInterface import OrganizationRepositoryInterface
from domain.Organization.OrganizationDomainModel import OrganizationDomainModel
from config.Database_config import get_database
from config.Logger_config import get_logger
from infrastructure.InfrastructureException import InfrastructureException

logger = get_logger(__name__)

class OrganizationMongoRepository(OrganizationRepositoryInterface):
    def __init__(self):
        self.db = None
        self.collection_name = "cdOrganization"
    
    async def _get_collection(self):
        if self.db is None:
            self.db = await get_database()
        return self.db[self.collection_name]
    
    def _to_domain_model(self, db_model: Dict[str, Any]) -> OrganizationDomainModel:
        """Convierte un documento de MongoDB a un modelo de dominio"""
        if not db_model:
            return None
        
        return OrganizationDomainModel(
            organization=db_model["organization"]
        )
    
    def _to_db_model(self, domain_model: OrganizationDomainModel) -> Dict[str, Any]:
        """Convierte un modelo de dominio a un documento de MongoDB"""
        return {
            "organization": domain_model.organization
        }
    
    async def save(self, organization: OrganizationDomainModel) -> str:
        """
        Guarda una organización en la base de datos.
        
        Args:
            organization: Modelo de dominio de la organización
            
        Returns:
            ID de la organización guardada
        """
        try:
            collection = await self._get_collection()
            db_model = self._to_db_model(organization)
            
            # Verificar si ya existe una organización con este ID
            existing_org = await collection.find_one({"organization": organization.organization})
            if existing_org:
                # La organización ya existe, no es necesario actualizarla
                logger.info(f"Organización ya existente: {organization.organization}")
            else:
                # Insertar nueva organización
                result = await collection.insert_one(db_model)
                logger.info(f"Organización guardada: {organization.organization}")
            
            return organization.organization
        except Exception as e:
            logger.error(f"Error al guardar organización: {e}")
            raise InfrastructureException(f"Error al guardar organización: {e}")
    
    async def find_by_id(self, organization_id: str) -> Optional[OrganizationDomainModel]:
        """
        Busca una organización por su ID.
        
        Args:
            organization_id: ID de la organización a buscar
            
        Returns:
            Modelo de dominio de la organización, o None si no se encuentra
        """
        try:
            collection = await self._get_collection()
            db_model = await collection.find_one({"organization": organization_id})
            if not db_model:
                return None
            
            return self._to_domain_model(db_model)
        except Exception as e:
            logger.error(f"Error al buscar organización por ID: {e}")
            raise InfrastructureException(f"Error al buscar organización por ID: {e}")
    
    async def get_all(self) -> List[OrganizationDomainModel]:
        """
        Obtiene todas las organizaciones registradas.
        
        Returns:
            Lista de modelos de dominio de organizaciones
        """
        try:
            collection = await self._get_collection()
            cursor = collection.find()
            organizations = []
            
            async for db_model in cursor:
                organization = self._to_domain_model(db_model)
                organizations.append(organization)
            
            return organizations
        except Exception as e:
            logger.error(f"Error al obtener todas las organizaciones: {e}")
            raise InfrastructureException(f"Error al obtener todas las organizaciones: {e}") 