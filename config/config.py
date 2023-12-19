import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

load_dotenv()

CATEGORY_VALUES = {
    'PH': 0.08,
    'ID': 1,
    'CG': 0.5,
    'DT': 0.125,
    'PG': 0,
}

BOT_TOKEN = os.getenv('BOT')
ADMIN_IDS = os.getenv('ADMIN')
storage = MemoryStorage()

bot = Bot(BOT_TOKEN)
dp = Dispatcher(bot, storage=storage)
