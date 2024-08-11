from src.external.telegram.service import TelegramService
from src.utils import HTMLFormatter
from src.utils import SingletonMeta

from .schemas import CreateCommunicationRequest


class CommunicationRequestsService(metaclass=SingletonMeta):
    telegram_service = TelegramService()
    html_formatter = HTMLFormatter()

    async def send_new_communication_request_message_to_admins(self, data: CreateCommunicationRequest):
        await self.telegram_service.notify_in_admin_group(
            f"{self.html_formatter.bold("Новая заявка:")}\n\n"
            f"{data.name + "\n" if data.name else ""}"
            f"{data.contact_type.capitalize()}: {data.value}"
        )
