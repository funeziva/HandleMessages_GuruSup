from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ServerSelectionTimeoutError, ConnectionFailure
from config.Logger_config import get_logger
from config.Settings import settings

logger = get_logger(__name__)

# Configuración de MongoDB
MONGODB_URI = settings.MONGODB_URI
MONGODB_DB = settings.MONGODB_DB

# Cliente de MongoDB
client = None
db = None

async def connect_to_mongodb():
    global client, db
    try:
        # Opciones de conexión para mejorar la robustez usando la configuración
        client = AsyncIOMotorClient(
            MONGODB_URI,
            minPoolSize=settings.MONGODB_MIN_POOL_SIZE,
            maxPoolSize=settings.MONGODB_MAX_POOL_SIZE,
            serverSelectionTimeoutMS=settings.MONGODB_SERVER_SELECTION_TIMEOUT_MS,
            connectTimeoutMS=settings.MONGODB_CONNECT_TIMEOUT_MS,
            socketTimeoutMS=settings.MONGODB_SOCKET_TIMEOUT_MS,
            retryWrites=settings.MONGODB_RETRY_WRITES,
            w="majority"  # Esperar confirmación de la mayoría de nodos
        )
        
        # Verificar que podemos conectarnos al servidor
        await client.admin.command('ping')
        
        db = client[MONGODB_DB]
        logger.info(f"Conexión a MongoDB establecida correctamente en {MONGODB_URI}")
        
        # Crear índices necesarios de forma más robusta
        await create_indexes()
        
        return db
    except (ServerSelectionTimeoutError, ConnectionFailure) as e:
        logger.error(f"No se pudo conectar a MongoDB: {e}")
        raise
    except Exception as e:
        logger.error(f"Error al conectar a MongoDB: {e}")
        raise

async def create_indexes():
    """Función separada para crear índices con manejo de errores específico"""
    try:
        # Crear índices con opciones adicionales
        await db.cdMessages.create_index([("PID", 1)], unique=True, background=True)
        await db.cdThread.create_index([("FID", 1)], unique=True, background=True)
        await db.cdOrganization.create_index([("organization", 1)], unique=True, background=True)
        await db.cdUsers.create_index([("email", 1)], unique=True, background=True)
        
        # Índices adicionales para búsquedas comunes
        await db.cdMessages.create_index([("organization", 1), ("thread_id", 1)], background=True)
        await db.cdThread.create_index([("organization", 1)], background=True)
        await db.cdUsers.create_index([("organization", 1)], background=True)
        
        logger.info("Índices de MongoDB creados correctamente")
    except Exception as e:
        logger.error(f"Error al crear índices en MongoDB: {e}")
        # No levantamos la excepción para permitir que la aplicación funcione
        # aún sin índices optimizados

async def get_database():
    if db is None:
        await connect_to_mongodb()
    return db

async def close_mongodb_connection():
    global client
    if client:
        client.close()
        logger.info("Conexión a MongoDB cerrada")

async def check_connection_health():
    """Función para verificar la salud de la conexión a MongoDB"""
    try:
        if client is None:
            return False
        
        # Verificar si podemos realizar una operación simple
        await client.admin.command('ping')
        return True
    except Exception as e:
        logger.error(f"Error en la verificación de salud de MongoDB: {e}")
        return False 