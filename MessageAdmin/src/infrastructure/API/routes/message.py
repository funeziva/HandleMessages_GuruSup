from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from config.Database_config import get_database
from config.Logger_config import get_logger
from domain.Message.MessageDomainModel import MessageDomainModel
from domain.Message.MessageRepositoryInterface import MessageRepositoryInterface
from infrastructure.MongoDB.MessageMongoRepository import MessageMongoRepository

logger = get_logger(__name__)

router = APIRouter(
    prefix="/messages",
    tags=["Messages"],
    responses={404: {"description": "Message not found"}},
)

async def get_message_repository():
    db = await get_database()
    return MessageMongoRepository(db)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=MessageDomainModel)
async def create_message(
    message: MessageDomainModel,
    repo: MessageRepositoryInterface = Depends(get_message_repository)
):
    """Crea un nuevo mensaje"""
    try:
        result = await repo.save(message)
        return result
    except Exception as e:
        logger.error(f"Error al crear el mensaje: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al crear el mensaje: {str(e)}",
        )

@router.get("/", response_model=List[MessageDomainModel])
async def read_messages(
    skip: int = 0,
    limit: int = 100,
    repo: MessageRepositoryInterface = Depends(get_message_repository)
):
    """Obtiene todos los mensajes"""
    messages = await repo.find_by_organization(None)  # Si no se especifica organización, obtener todos
    return messages[skip:skip + limit]

@router.get("/{message_id}", response_model=MessageDomainModel)
async def read_message(
    message_id: str,
    repo: MessageRepositoryInterface = Depends(get_message_repository)
):
    """Obtiene un mensaje por ID"""
    message = await repo.find_by_id(message_id)
    if message is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Mensaje no encontrado",
        )
    return message

@router.get("/thread/{thread_id}", response_model=List[MessageDomainModel])
async def read_thread_messages(
    thread_id: str,
    repo: MessageRepositoryInterface = Depends(get_message_repository)
):
    """Obtiene todos los mensajes de un hilo"""
    messages = await repo.find_by_organization(thread_id)  # Usando el thread_id como organización temporalmente
    return messages 