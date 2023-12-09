from typing import Union

from aiogram.types import Message, CallbackQuery
from aiogram import types

from data.config import ADMINS
from data.products import create_product_invoice, REGULAR_EXPRESS, FAST_EXPRESS, PICKUP_EXPRESS
from keyboards.inline import menu_cd, buy_cd, categories_keyboards, products_keyboards, product_keyboards
from loader import dp, db, bot


@dp.message_handler(text="Menu categories")
async def menu(msg: Message):
    await list_categories(msg)


async def list_categories(message: Union[Message, CallbackQuery], **kwargs):
    if isinstance(message, Message):
        await message.answer("Kategoriyani tanlang:", reply_markup=await categories_keyboards())
    elif isinstance(message, CallbackQuery):
        call = message
        await call.message.edit_text("Kategoriyani tanlang:", reply_markup=await categories_keyboards())


async def list_products(call: CallbackQuery, category_id, **kwargs):
    await call.message.edit_text("Mahsulotni tanlang:", reply_markup=await products_keyboards(category_id))


async def show_product(call: CallbackQuery, category_id, item_id, **kwargs):
    product = db.select_product(item_id)
    brand = product[1]
    desc = product[2]
    price = product[3]
    image = product[4]
    category_id = product[5]
    info = f"<b>Brand</b>\n{brand}\n\n" \
           f"<b>Izoh</b>\n{desc}\n\n" \
           f"<b>Narxi</b>: <tg-spoiler>${price}</tg-spoiler>\n\n" \
           f"<i><b>Kategory: {db.select_category(category_id)[1]}</b></i>"
    if image:
        await call.message.answer_photo(image, caption=info, reply_markup=await product_keyboards(item_id))
    else:
        await call.message.answer(info, reply_markup=await product_keyboards(item_id))


async def remove_item(call: CallbackQuery, **kwargs):
    await call.message.delete()


@dp.callback_query_handler(menu_cd.filter())
async def callback_handler(call: CallbackQuery, callback_data: dict):
    level = callback_data.get('level')
    category_id = callback_data.get('category_id')
    item_id = callback_data.get('item_id')

    levels = {
        '0': list_categories,
        '1': list_products,
        '2': show_product,
        '3': remove_item
    }

    current_func = levels[level]
    await current_func(call, category_id=category_id, item_id=item_id)


@dp.callback_query_handler(buy_cd.filter())
async def buy_item(call: CallbackQuery, callback_data: dict):
    item_id = callback_data.get('item_id')
    data = create_product_invoice(db.select_product(item_id))
    await bot.send_invoice(call.from_user.id, **data.generate_invoice(), payload=f'{item_id}')


@dp.shipping_query_handler()
async def choose_shipping(query: types.ShippingQuery):
    if query.shipping_address.country_code != "UZ":
        await bot.answer_shipping_query(shipping_query_id=query.id,
                                        ok=False,
                                        error_message="Chet elga yetkazib bera olmaymiz")
    elif query.shipping_address.city.lower() == "toshkent":
        await bot.answer_shipping_query(shipping_query_id=query.id,
                                        shipping_options=[REGULAR_EXPRESS, FAST_EXPRESS, PICKUP_EXPRESS],
                                        ok=True)
    else:
        await bot.answer_shipping_query(shipping_query_id=query.id,
                                        shipping_options=[REGULAR_EXPRESS, FAST_EXPRESS],
                                        ok=True)


@dp.pre_checkout_query_handler()
async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query_id=pre_checkout_query.id,
                                        ok=True)
    await bot.send_message(chat_id=pre_checkout_query.from_user.id,
                           text="Xaridingiz uchun rahmat!")
    await bot.send_message(chat_id=ADMINS[0],
                           text=f"Quyidagi mahsulot sotildi: {pre_checkout_query.invoice_payload}\n"
                                f"ID: {pre_checkout_query.id}\n"
                                f"Telegram user: {pre_checkout_query.from_user.first_name}\n"
                                f"Xaridor: {pre_checkout_query.order_info.name}, tel: {pre_checkout_query.order_info.phone_number}")
