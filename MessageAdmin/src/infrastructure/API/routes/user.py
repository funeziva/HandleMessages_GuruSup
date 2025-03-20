from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from config.Database_config import get_database
from config.Logger_config import get_logger
from domain.User.UserDomainModel import UserDomainModel
from domain.User.UserRepositoryInterface import UserRepositoryInterface
from infrastructure.MongoDB.UserMongoRepository import UserMongoRepository

logger = get_logger(__name__)

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={404: {"description": "User not found"}},
)

async def get_user_repository():
    db = await get_database()
    return UserMongoRepository(db)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserDomainModel)
async def create_user(
    user: UserDomainModel,
    repo: UserRepositoryInterface = Depends(get_user_repository)
):
    """
    Crea un nuevo usuario
    """
    try:
        result = await repo.save(user)
        return result
    except Exception as e:
        logger.error(f"Error al crear el usuario: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al crear el usuario: {str(e)}",
        )

@router.get("/", response_model=List[UserDomainModel])
async def read_users(
    skip: int = 0,
    limit: int = 100,
    repo: UserRepositoryInterface = Depends(get_user_repository)
):
    """
    Obtiene todos los usuarios
    """
    users = await repo.get_all()
    return users[skip : skip + limit]

@router.get("/{user_id}", response_model=UserDomainModel)
async def read_user(
    user_id: str,
    repo: UserRepositoryInterface = Depends(get_user_repository)
):
    """
    Obtiene un usuario por ID
    """
    user = await repo.find_by_id(user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado",
        )
    return user

@router.get("/email/{email}", response_model=UserDomainModel)
async def read_user_by_email(
    email: str,
    repo: UserRepositoryInterface = Depends(get_user_repository)
):
    """
    Obtiene un usuario por email
    """
    user = await repo.find_by_email(email)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado",
        )
    return user

@router.get("/organization/{organization_id}", response_model=List[UserDomainModel])
async def read_organization_users(
    organization_id: str,
    repo: UserRepositoryInterface = Depends(get_user_repository)
):
    """
    Obtiene todos los usuarios de una organización
    """
    users = await repo.find_by_organization(organization_id)
    return users
