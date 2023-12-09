from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import ContentType

from keyboards.default import phone_button, menu_button
from loader import dp, db


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message, state: FSMContext):
    user = db.select_user(message.from_user.id)
    if user:
        await message.answer("Bot qayta ishga tushdi!", reply_markup=menu_button)
        return 
    await message.answer(f"Salom, {message.from_user.full_name}!\n"
                         f"Botdan foydalanish uchun kontaktni yuboring!", reply_markup=phone_button)
    await state.set_state("phone_number")


@dp.message_handler(state='phone_number', content_types='contact', is_sender_contact=True)
async def send_contact(msg: types.Message, state: FSMContext):
    user_id = msg.from_user.id
    fullname = msg.from_user.full_name
    number = msg.contact.phone_number
    mention = msg.from_user.get_mention()
    db.add_user(user_id, fullname, number, mention)
    await msg.answer("Botdan foydalanishingiz mumkin!", reply_markup=menu_button)
    await state.finish()


@dp.message_handler(state='phone_number', content_types=ContentType.ANY)
async def err_send_contact(msg: types.Message, state: FSMContext):
    await msg.answer("Botdan foydalanish uchun kontaktni yuboring!", reply_markup=phone_button)
