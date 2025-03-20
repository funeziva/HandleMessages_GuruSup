from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from config.Database_config import get_database
from config.Logger_config import get_logger
from domain.Thread.ThreadDomainModel import ThreadDomainModel
from domain.Thread.ThreadRepositoryInterface import ThreadRepositoryInterface
from infrastructure.MongoDB.ThreadMongoRepository import ThreadMongoRepository
from infrastructure.MongoDB.MessageMongoRepository import MessageMongoRepository
from application.Thread.GetThreadUseCase import GetThreadUseCase
from application.Thread.AddMessageToThreadUseCase import AddMessageToThreadUseCase

logger = get_logger(__name__)

router = APIRouter(
    prefix="/threads",
    tags=["Threads"],
    responses={404: {"description": "Thread not found"}},
)

async def get_thread_repository():
    db = await get_database()
    return ThreadMongoRepository(db)

async def get_message_repository():
    db = await get_database()
    return MessageMongoRepository(db)

# Dependencia para obtener el caso de uso para consultas
async def get_thread_use_case():
    thread_repo = await get_thread_repository()
    return GetThreadUseCase(thread_repo)

# Dependencia para obtener el caso de uso para añadir mensajes
async def get_add_message_use_case():
    thread_repo = await get_thread_repository()
    message_repo = await get_message_repository()
    return AddMessageToThreadUseCase(thread_repo, message_repo)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ThreadDomainModel)
async def create_thread(
    thread: ThreadDomainModel,
    repo: ThreadRepositoryInterface = Depends(get_thread_repository)
):
    """Crea un nuevo hilo"""
    try:
        result = await repo.save(thread)
        return result
    except Exception as e:
        logger.error(f"Error al crear el hilo: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al crear el hilo: {str(e)}",
        )

@router.get("/", response_model=List[ThreadDomainModel])
async def read_threads(
    skip: int = 0,
    limit: int = 100,
    repo: ThreadRepositoryInterface = Depends(get_thread_repository)
):
    """Obtiene todos los hilos"""
    threads = await repo.find_by_organization(None)  # Si no se especifica organización, obtener todos
    return threads[skip:skip + limit]

@router.get("/{thread_id}", response_model=ThreadDomainModel)
async def read_thread(
    thread_id: str,
    repo: ThreadRepositoryInterface = Depends(get_thread_repository)
):
    """Obtiene un hilo por ID"""
    thread = await repo.find_by_id(thread_id)
    if thread is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Hilo no encontrado",
        )
    return thread

@router.get("/organization/{organization_id}", response_model=List[ThreadDomainModel])
async def read_organization_threads(
    organization_id: str,
    repo: ThreadRepositoryInterface = Depends(get_thread_repository)
):
    """Obtiene todos los hilos de una organización"""
    threads = await repo.find_by_organization(organization_id)
    return threads

@router.post("/{thread_id}/messages/{message_id}")
async def add_message_to_thread(
    thread_id: str,
    message_id: str,
    use_case: AddMessageToThreadUseCase = Depends(get_add_message_use_case)
):
    """
    Añade un mensaje a un hilo existente.
    """
    try:
        result = await use_case.execute(thread_id, message_id)
        if not result:
            raise HTTPException(status_code=400, detail="No se pudo añadir el mensaje al hilo")
        return {"success": True, "message": f"Mensaje {message_id} añadido al hilo {thread_id}"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error al añadir mensaje {message_id} al hilo {thread_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e)) 