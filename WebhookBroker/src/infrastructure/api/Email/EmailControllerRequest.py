from pydantic import BaseModel
from typing import Dict, Any

class EmailControllerRequest(BaseModel):
    attachments: int
    subject: str
    charsets: Dict[str, str]
    dkim: Dict[str, Any]
    sender_ip: str
    SPF: str
    to: str
    text: str
    html: str
    headers: str
    from_: str
    envelope: Dict[str, Any]
    attachment_info: Dict[str, Any]
    content_ids: Dict[str, Any]
