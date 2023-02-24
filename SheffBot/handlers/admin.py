from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from venv3.create_bot import bot,dp
from aiogram.dispatcher.filters import Text
from data_base import sqlite_dp
from keyboards import keyboards_for_admin
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

ID = None


class FSMAdmin(StatesGroup):
    photo = State()
    name = State()
    description = State()
    price = State()
    status = State()


#@dp.message_handler(commands=['moderator'], is_chat_admin=True)
async def make_changes_command(message: types.Message):
    global ID
    ID = message.from_user.id
    await bot.send_message(message.from_user.id, 'Здравствуйте, начальник', reply_markup=keyboards_for_admin.button_case_admin)
    await message.delete()


#@dp.message_handler(commands='Загрузить_Товар', state=None)
async def add_clothes(message : types.Message):
    if message.from_user.id == ID:
        await FSMAdmin.photo.set()
        await message.reply('Отправь фото товара')


#@dp.message_handler(state="*", commands='отмена')
#@dp.message_handler(Text(equals='отмена', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await message.reply('Загрузка товара отменена')


#@dp.message_handler(content_types=['photo'], state=FSMAdmin.photo)
async def send_photo(message : types.Message, state : FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['photo'] = message.photo[0].file_id
        await FSMAdmin.next()
        await message.reply('Теперь введи название товара')


#@dp.message_handler(content_types=['name'], state=FSMAdmin.name)
async def send_name(message : types.Message, state : FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['name'] = message.text
        await FSMAdmin.next()
        await  message.reply('Опиши состояние и материалы')


#@dp.message_handler(content_types=['description'], state=FSMAdmin.description)
async def send_description(message : types.Message, state : FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['description'] = message.text
        await FSMAdmin.next()
        await  message.reply('Укажи цену')


# @dp.message_handler(content_types=['price'], state=FSMAdmin.price)
async def send_price(message : types.Message, state : FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['price'] = float(message.text)

        await sqlite_dp.sql_add_command(state)
        await state.finish()


@dp.callback_query_handlers(lambda x: x.data and x.data.startswith('del '))
async def del_callback_command(callback_query: types.CallbackQuery):
    await sqlite_dp.sql_delete_command(callback_query.data.replace('del ', ''))
    await callback_query.answer(text=f'{callback_query.data.replace("del ", "")} удалена', show_alert=True)


@dp.message_handler(commands='Удалить')
async def del_item(message: types.Message):
    if message.from_user.id == ID:
        read = await sqlite_dp.sql_read2()
        for ret in read:
            await bot.send_photo(message.from_user.id, ret[0], f'{ret[1]}\nОписание: {ret[2]}\nЦена: {ret[-1]}')
            await bot.send_message(message.from_user.id, text='^^^', reply_markup=InlineKeyboardMarkup().\
                                   add(InlineKeyboardButton(f'Удалить {ret[1]}', callback_data=f'del {ret[1]}')))


def register_handler_admin(dp : Dispatcher):
    dp.register_message_handler(add_clothes, commands=['Загрузить_Товар'])
    dp.register_message_handler(send_photo, content_types=['photo'], state=FSMAdmin.photo)
    dp.register_message_handler(send_name, state=FSMAdmin.name)
    dp.register_message_handler(send_description, state=FSMAdmin.description)
    dp.register_message_handler(send_price, state=FSMAdmin.price)
    dp.register_message_handler(cancel_handler, state="*", commands='отмена')
    dp.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state='*')
    dp.register_message_handler(make_changes_command, commands=['moderator'], is_chat_admin=True)