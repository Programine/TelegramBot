from aiogram import types, Dispatcher
from venv3.create_bot import bot, dp
from keyboards import kb_client
from data_base import sqlite_dp

#@dp.message_handler(commands=['start', 'help'])
async def commands_start(message : types.Message):
    try:
        await bot.send_message(message.from_user.id, 'Привет, ты попал в наш магазин Одеждый. Тут для себя найдет что то интерессное каждый!', reply_markup=kb_client)
        await message.delete()
    except:
        await message.reply('Для общения с ботом через ЛС, напишите ему:\n')

#@dp.message_handler(commands='Местоположение')
async def command_geo(message : types.Message):
    await bot.send_message(message.from_user.id, 'ул.Одесская 341')

#@dp.message_handler(commands='Режим_работы')
async def command_graph(message : types.Message):
    await bot.send_message(message.from_user.id, '===Режим работы===\nПонедельник: 9:00 - 22:00\nВторник: 9:00 - 22:00\nСреда: 9:00 - 22:00\Четверг: 9:00 - 22:00\nПятница: 9:00 - 22:00\nСуббота: 9:00 - 20:00\nВоскресенье: 9:00 - 23:00')

@dp.message_handler(commands=['Меню'])
async def cloth_menu(message: types.Message):
   await sqlite_dp.sql_read(message)


def register_handler_client(dp : Dispatcher):
    dp.register_message_handler(commands_start, commands=['start', 'help'])
    dp.register_message_handler(command_geo, commands=['Местоположение'])
    dp.register_message_handler(command_graph, commands=['Режим_работы'])
    dp.register_message_handler(cloth_menu, commands=['Меню'])

