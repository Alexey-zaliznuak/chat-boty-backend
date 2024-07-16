from pydantic import BaseModel, Field, model_validator
from pydantic.class_validators import root_validator
from typing import Union
import re
from enum import Enum


class ContactType(str, Enum):
    telegram = "telegram"
    phone = "phone"


class CreateCommunicationRequest(BaseModel):
    contact_type: ContactType
    value: str

    @model_validator(mode="after")
    def check_value(self):
        if self.contact_type == ContactType.telegram:
            if not re.match(r'^[a-zA-Z0-9_]{5,32}$', self.value):
                raise ValueError('Invalid Telegram username. It should be 5-32 characters long and can contain letters, numbers, and underscores.')

        elif self.contact_type == ContactType.phone:
            if not re.match(r'^\+7\d{10}$', self.value):
                raise ValueError('Invalid phone number. It should be a valid Russian phone number in the format +7XXXXXXXXXX.')

        return self
