from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from config.Database_config import get_database
from config.Logger_config import get_logger
from domain.Organization.OrganizationDomainModel import OrganizationDomainModel
from domain.Organization.OrganizationRepositoryInterface import OrganizationRepositoryInterface
from infrastructure.MongoDB.OrganizationMongoRepository import OrganizationMongoRepository

logger = get_logger(__name__)

router = APIRouter(
    prefix="/organizations",
    tags=["Organization"],
    responses={404: {"description": "Organization not found"}},
)

# Dependencia para obtener el repositorio
async def get_organization_repository():
    db = await get_database()
    return OrganizationMongoRepository(db)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=OrganizationDomainModel)
async def create_organization(
    organization: OrganizationDomainModel,
    repo: OrganizationRepositoryInterface = Depends(get_organization_repository)
):
    """Crea una nueva organización"""
    try:
        result = await repo.save(organization)
        return result
    except Exception as e:
        logger.error(f"Error al crear la organización: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al crear la organización: {str(e)}",
        )

@router.get("/", response_model=List[OrganizationDomainModel])
async def read_organizations(
    skip: int = 0,
    limit: int = 100,
    repo: OrganizationRepositoryInterface = Depends(get_organization_repository)
):
    """Obtiene todas las organizaciones"""
    organizations = await repo.get_all(skip, limit)
    return organizations

@router.get("/{organization_id}", response_model=OrganizationDomainModel)
async def read_organization(
    organization_id: str,
    repo: OrganizationRepositoryInterface = Depends(get_organization_repository)
):
    """Obtiene una organización por ID"""
    organization = await repo.find_by_id(organization_id)
    if organization is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organización no encontrada",
        )
    return organization 