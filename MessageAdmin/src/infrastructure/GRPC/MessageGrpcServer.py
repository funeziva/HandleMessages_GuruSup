import asyncio
import grpc
from concurrent import futures
from config.GRPC_config import GRPC_HOST, GRPC_PORT
from config.Logger_config import get_logger
from infrastructure.GRPC.EmailServicer import EmailServicer
from infrastructure.GRPC.WhatsAppServicer import WhatsAppServicer
from infrastructure.GRPC.generated import message_service_pb2_grpc

logger = get_logger(__name__)

class MessageGrpcServer:
    def __init__(self, host=GRPC_HOST, port=GRPC_PORT):
        self.host = host
        self.port = port
        self.server = None
    
    async def start(self):
        """
        Inicia el servidor gRPC.
        """
        try:
            # Crear servidor gRPC
            self.server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=10))
            
            # Añadir servicios al servidor
            message_service_pb2_grpc.add_EmailServiceServicer_to_server(
                EmailServicer(), self.server
            )
            message_service_pb2_grpc.add_WhatsAppServiceServicer_to_server(
                WhatsAppServicer(), self.server
            )
            
            # Añadir dirección de escucha
            address = f"{self.host}:{self.port}"
            self.server.add_insecure_port(address)
            
            # Iniciar el servidor
            await self.server.start()
            logger.info(f"Servidor gRPC iniciado en {address}")
            
            # Esperar a que el servidor se detenga
            await self.server.wait_for_termination()
            
        except Exception as e:
            logger.error(f"Error al iniciar el servidor gRPC: {e}")
            raise
    
    async def stop(self):
        """
        Detiene el servidor gRPC.
        """
        if self.server:
            await self.server.stop(0)
            logger.info("Servidor gRPC detenido") 