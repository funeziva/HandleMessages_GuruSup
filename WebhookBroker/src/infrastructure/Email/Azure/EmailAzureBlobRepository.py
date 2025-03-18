import json
from azure.storage.blob.aio import BlobServiceClient
from azure.core.exceptions import AzureError
from config.Logger_config import get_logger
from domain.Email.EmailAzureBlobRepositoryInterface import EmailAzureBlobRepositoryInterface
from domain.Email.EmailDomainModel import EmailDomainModel
from infrastructure.InfrastructureException import InfrastructureException
from config.Logger_config import get_logger

logger = get_logger(__name__)

class EmailAzureBlobRepository(EmailAzureBlobRepositoryInterface):
    def __init__(self, connection_string: str, container_name: str):
        self.connection_string = connection_string
        self.container_name = container_name
        self.blob_service_client = BlobServiceClient.from_connection_string(self.connection_string)
        self.container_client = None

    async def init_container(self):
        """
        Inicializa el container en Azure Blob Storage. Si el contenedor ya existe, se ignora el error.
        """
        logger.info(f"[AzureStorageAdapter] Inicializando contenedor: {self.container_name}")
        self.container_client = self.blob_service_client.get_container_client(self.container_name)
        try:
            await self.container_client.create_container()
        except Exception:
            # El contenedor ya existe, ignoramos el error.
            pass

    async def saveEmail(self, email: EmailDomainModel) -> None:
        """
        Guarda el email en Azure Blob Storage de forma asíncrona.
        Lanza excepciones si ocurre algún error durante la subida.
        """
        try:
            if self.container_client is None:
                await self.init_container()


            # Generar un nombre único para el blob (por ejemplo, usando sender_ip y subject)
            blob_name = f"{email.from_}_{email.subject}.json"
            logger.info(f"[AzureStorageAdapter] Guardando email en Azure Blob: {blob_name}")
            data_to_store = email.dict()
            data_json = json.dumps(data_to_store)
            await self.container_client.upload_blob(name=blob_name, data=data_json, overwrite=True)
            logger.info(f"[AzureStorageAdapter] Email guardado en Azure Blob: {blob_name}")
        except AzureError as e:
            logger.error(f"[AzureStorageAdapter] Error al guardar email en Azure Blob: {e}")
            raise InfrastructureException(f"Error uploading to Azure Blob", e)
        except Exception as e:
            logger.error(f"[AzureStorageAdapter] Error al guardar email en Azure Blob: {e}")
            raise InfrastructureException(f"Error inesperado al guardar email", e)
