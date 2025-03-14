import asyncio
from application.Email.EmailUserCaseModel import EmailUserCaseModel
from domain.Email.EmailEventPublisherInterface import EmailEventPublisherInterface
from domain.Email.EmailAzureBlobRepositoryInterface import EmailAzureBlobRepositoryInterface
from domain.Email.EmailDomainModel import EmailDomainModel

class HandleEmailUserCase:
    """
    Caso de uso para procesar un EmailEntity.
    """

    def __init__(self, emailAzureBlobRepository: EmailAzureBlobRepositoryInterface, emailEventPublisher: EmailEventPublisherInterface):
        self.emailAzureBlobRepository = emailAzureBlobRepository
        self.emailEventPublisher = emailEventPublisher

    async def handle_incoming_email(self, email: EmailUserCaseModel):
        # Convertir la entidad de aplicación a la entidad de dominio
        domain_model = EmailDomainModel(
            attachments=email.attachments,
            subject=email.subject,
            charsets=email.charsets,
            dkim=email.dkim,
            sender_ip=email.sender_ip,
            SPF=email.SPF,
            to=email.to,
            text=email.text,
            html=email.html,
            headers=email.headers,
            from_=email.from_,
            envelope=email.envelope,
            attachment_info=email.attachment_info,
            content_ids=email.content_ids
        )

        # Llamada asíncrona para el repositorio de Azure
        await self.emailAzureBlobRepository.saveEmail(domain_model)
        
        # Llamada sincrónica para publicar el evento
        # Si este método es rápido y no bloquea, puedes llamarlo directamente;
        # de lo contrario, envolverlo en asyncio.to_thread es recomendable.
        await asyncio.to_thread(self.emailEventPublisher.publish_email_event, domain_model)


