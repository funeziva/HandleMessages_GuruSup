from fastapi import APIRouter, status, Depends, HTTPException
from config.Logger_config import get_logger
from domain.DomainException import DomainException
from application.Email.EmailUserCaseModel import EmailUserCaseModel
from application.Email.HandleEmailUserCase import HandleEmailUserCase
from application.ApplicationException import ApplicationException
from infrastructure.InfrastructureException import InfrastructureException
from infrastructure.api.Email.EmailControllerRequest import EmailControllerRequest
from infrastructure.Email.Dependencies.GetHandleEmailUserCase import get_HandleEmailUserCase

EmailRouter = APIRouter(prefix="/v1/email", tags=["Email"])
logger = get_logger("uvicorn")

@EmailRouter.post("/webhook", status_code=status.HTTP_200_OK)
async def receive_email_webhook(
    request: EmailControllerRequest,
    service: HandleEmailUserCase = Depends(get_HandleEmailUserCase)
):
    
    logger.info(f"Received email webhook: {request}")

    try:
        email_entity = EmailUserCaseModel(
            attachments=request.attachments,
            subject=request.subject,
            charsets=request.charsets,
            dkim=request.dkim,
            sender_ip=request.sender_ip,
            SPF=request.SPF,
            to=request.to,
            text=request.text,
            html=request.html,
            headers=request.headers,
            from_=request.from_,
            envelope=request.envelope,
            attachment_info=request.attachment_info,
            content_ids=request.content_ids,
        )

        await service.handle_incoming_email(email_entity)

        return {"message": "OK"}

    except ApplicationException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except DomainException as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))
    except InfrastructureException as e:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
