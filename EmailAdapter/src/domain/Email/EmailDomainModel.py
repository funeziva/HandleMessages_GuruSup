from dataclasses import dataclass, field
from typing import List, Dict, Optional

@dataclass
class EmailDomainModel:
    id: str
    subject: str
    body: str
    sender: str
    recipients: List[str] = field(default_factory=list)
    # attachments: List[str] = field(default_factory=list)

    def __post_init__(self):
        if not self.id:
            raise ValueError("El campo 'id' es obligatorio.")
        if not self.subject:
            raise ValueError("El campo 'subject' es obligatorio.")
        if not self.body:
            raise ValueError("El campo 'body' es obligatorio.")
        if not self.sender:
            raise ValueError("El campo 'sender' es obligatorio.")
        if not self.recipients:
            raise ValueError("El campo 'recipients' es obligatorio.")
