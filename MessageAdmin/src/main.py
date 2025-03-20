import asyncio
import uvicorn
from config.API_config import API_HOST, API_PORT
from config.Logger_config import get_logger
from infrastructure.GRPC.MessageGrpcServer import MessageGrpcServer

logger = get_logger(__name__)

async def start_grpc_server():
    """Inicia el servidor gRPC"""
    server = MessageGrpcServer()
    await server.start()

async def start_api_server():
    """Inicia el servidor FastAPI"""
    config = uvicorn.Config(
        "infrastructure.API.app:app",
        host=API_HOST,
        port=API_PORT,
        log_level="info",
        reload=True
    )
    server = uvicorn.Server(config)
    await server.serve()

async def main():
    """Inicia ambos servidores en tareas concurrentes"""
    try:
        # Crear tareas para ambos servidores
        grpc_task = asyncio.create_task(start_grpc_server())
        api_task = asyncio.create_task(start_api_server())
        
        # Esperar a que ambas tareas completen
        await asyncio.gather(grpc_task, api_task)
    except Exception as e:
        logger.error(f"Error en la aplicación principal: {e}")
        raise

if __name__ == "__main__":
    logger.info("Iniciando MessageAdmin...")
    asyncio.run(main()) 