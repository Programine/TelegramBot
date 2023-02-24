from aiogram import Bot
from aiogram.dispatcher import Dispatcher
import os
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()

bot = Bot(token='5888138978:AAGsLdWMHM5D_sP4Uzqw4xxskxp3_CXm9uU')
dp = Dispatcher(bot, storage=storage)