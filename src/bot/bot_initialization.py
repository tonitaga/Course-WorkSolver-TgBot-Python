import os

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv

load_dotenv('.env')
token_api = os.getenv("TOKEN_API")

bot = Bot(token_api)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
