from aiogram.utils import executor
from venv3.create_bot import dp
import logging
from data_base import sqlite_dp

logging.basicConfig(filename='../bot.log', level=logging.INFO)

async def on_startup(_):
    print('Бот на месте')
    sqlite_dp.sql_start()


from handlers import client, admin, other

client.register_handler_client(dp)
admin.register_handler_admin(dp)
other.register_handler_other(dp)


executor.start_polling(dp, skip_updates=True, on_startup=on_startup)