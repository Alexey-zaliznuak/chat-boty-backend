import asyncio

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from src.utils import SingletonMeta

from src.config import Config


class TelegramService(metaclass=SingletonMeta):
    ADMIN_CHAT_ID = Config.TELEGRAM_ADMIN_CHAT_ID

    def __init__(self):
        self.__bot = Bot(
            token=Config.TELEGRAM_BOT_TOKEN,
            default=DefaultBotProperties(
                parse_mode=ParseMode.HTML,
            ),
        )

    async def notify_in_admin_group(self, message: str):
        await self.__bot.send_message(chat_id=self.ADMIN_CHAT_ID, text=message)
