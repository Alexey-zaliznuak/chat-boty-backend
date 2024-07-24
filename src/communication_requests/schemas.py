from pydantic import BaseModel
from enum import Enum


class ContactType(str, Enum):
    telegram = "telegram"
    phone = "phone"


class CreateCommunicationRequest(BaseModel):
    contact_type: ContactType
    name: str | None
    value: str
