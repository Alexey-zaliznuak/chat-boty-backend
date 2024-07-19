from src.external.telegram.service import TelegramService
from src.infrastructure.utils.html_formatter import HTMLFormatter
from src.infrastructure.utils.singleton import SingletonMeta

from .schemas import ContactType


class CommunicationRequestsService(metaclass=SingletonMeta):
    telegram_service = TelegramService()
    html_formatter = HTMLFormatter()

    async def send_new_communication_request_message_to_admins(self, contact: str, contact_type: ContactType):
        await self.telegram_service.notify_in_admin_group(
            f"{self.html_formatter.bold("Новая заявка:")}\n\n"
            f"{contact_type.capitalize()}: {("@" + contact)}"
        )
