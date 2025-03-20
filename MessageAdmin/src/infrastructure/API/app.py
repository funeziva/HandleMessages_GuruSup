from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config.Database_config import connect_to_mongodb, close_mongodb_connection
from config.Logger_config import get_logger
from infrastructure.API.routes import message, thread, organization, user

logger = get_logger(__name__)

app = FastAPI(
    title="MessageAdmin API",
    description="API para gestionar mensajes, hilos y organizaciones",
    version="1.0.0",
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, esto debería ser más restrictivo
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Eventos de inicio y cierre
@app.on_event("startup")
async def startup_db_client():
    try:
        await connect_to_mongodb()
        logger.info("Conexión a MongoDB establecida en el inicio de la aplicación")
    except Exception as e:
        logger.error(f"Error al conectar a MongoDB en el inicio: {e}")

@app.on_event("shutdown")
async def shutdown_db_client():
    try:
        await close_mongodb_connection()
        logger.info("Conexión a MongoDB cerrada al detener la aplicación")
    except Exception as e:
        logger.error(f"Error al cerrar la conexión a MongoDB: {e}")

# Incluir rutas
app.include_router(message.router)
app.include_router(thread.router)
app.include_router(organization.router)
app.include_router(user.router)

# Ruta raíz
@app.get("/")
async def root():
    return {"message": "Bienvenido a la API de MessageAdmin"} 