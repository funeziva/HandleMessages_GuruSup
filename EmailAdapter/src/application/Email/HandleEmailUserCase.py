# src/application/HandleIncomingEmailEventUseCase.py
import re
from domain.Email.EmailDomainModel import EmailDomainModel

def extract_message_id(headers: str) -> str:
    """
    Intenta extraer el Message-ID de los headers usando distintos patrones.
    Si no se encuentra, lanza un ValueError.
    """
    # Primer patrón: "Message-ID: <...>" o "Message-ID: ..."
    pattern1 = re.compile(r"Message-ID:\s*<?([^>\s]+)>?", re.IGNORECASE)
    match = pattern1.search(headers)
    if match:
        return match.group(1)
    
    # Segundo patrón: "message-id=321:" o similar
    pattern2 = re.compile(r"message-id=([^:\s]+):", re.IGNORECASE)
    match = pattern2.search(headers)
    if match:
        return match.group(1)
    
    raise ValueError("No se encontró el Message-ID en los headers.")

def create_EmailDomainModel(email_data: dict) -> EmailDomainModel:
    subject = email_data.get("subject", "").strip()
    html_body = email_data.get("html", "").strip()
    sender = email_data.get("from_", "").strip()
    recipient = email_data.get("to", "").strip()

    headers = email_data.get("headers", "")
    try:
        message_id = extract_message_id(headers)
    except Exception as e:
        raise ValueError(f"Error al procesar los headers: {e}")

    email_domain = EmailDomainModel(
        id=message_id,
        subject=subject,
        body=html_body,
        sender=sender,
        recipients=[recipient],
        # attachments=[],          
    )
    
    return email_domain

class HandleEmailUserCase:
    def __init__(self, grpc_client):
        self.grpc_client = grpc_client

    def execute(self, email_data: dict):
        
        email_domain = create_EmailDomainModel(email_data)

        print(f"[HandleIncomingEmailEventUseCase] Procesando email con ID: {email_domain.id}")
        self.grpc_client.send_email_to_message_admin(email_domain)
