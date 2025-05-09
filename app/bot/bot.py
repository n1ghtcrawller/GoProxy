import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from app.core.config import settings
from aiogram.types import Message


bot_logger = logging.getLogger("bot")
BOT_TOKEN = settings.BOT_TOKEN

dp = Dispatcher()
logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
async def start_bot():
    bot_logger.info("Запуск бота...")
    try:
        await dp.start_polling(bot)
        bot_logger.info("Бот запущен")
    except Exception as e:
        bot_logger.error(f"Ошибка при запуске бота: {str(e)}")
        raise

@dp.message(CommandStart())
async def command_start_handler(message: Message, chat_id) -> None:
    try:
        await message.answer("Добро пожаловать")
        bot_logger.info(f"Запущен бот пользователем {message.from_user}")
    except Exception as e:
        raise
