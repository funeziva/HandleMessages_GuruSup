from dataclasses import dataclass, field
from typing import List
from domain.DomainException import DomainException

@dataclass
class EmailDomainModel:
    id: str
    subject: str
    body: str
    sender: str
    text: str
    recipients: List[str] = field(default_factory=list)
    # attachments: List[str] = field(default_factory=list)

    def __post_init__(self):
        if not self.id:
            raise DomainException("El campo 'id' es obligatorio.")
        if not self.text:
            raise DomainException("El campo 'text' es obligatorio.")
        if not self.subject:
            raise DomainException("El campo 'subject' es obligatorio.")
        if not self.body:
            raise DomainException("El campo 'body' es obligatorio.")
        if not self.sender:
            raise DomainException("El campo 'sender' es obligatorio.")
        if not self.recipients:
            raise DomainException("El campo 'recipients' es obligatorio.")
