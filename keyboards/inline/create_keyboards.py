from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from loader import db

menu_cd = CallbackData('menu', 'level', 'category_id', 'item_id')
buy_cd = CallbackData('buy', 'item_id')


async def make_callback_data(level, category_id='0', item_id='0'):
    return menu_cd.new(level=level, category_id=category_id, item_id=item_id)


async def categories_keyboards():
    CURRENT_LEVEL = 0

    markup = InlineKeyboardMarkup(row_width=1)
    categories = db.select_categories()

    for category in categories:
        markup.insert(InlineKeyboardButton(
            text=category[1],
            callback_data=await make_callback_data(
                level=CURRENT_LEVEL + 1,
                category_id=category[0]
            )
        )
        )
    return markup


async def products_keyboards(category_id):
    CURRENT_LEVEL = 1

    markup = InlineKeyboardMarkup(row_width=1)
    products = db.select_category_products(category_id=category_id)

    for product in products:
        markup.insert(
            InlineKeyboardButton(
                text=product[1],
                callback_data=await make_callback_data(CURRENT_LEVEL + 1, category_id, item_id=product[0])
            )
        )
    markup.row(InlineKeyboardButton(
        text='🔙 Orqaga', callback_data=await make_callback_data(CURRENT_LEVEL - 1)
    ))

    return markup


async def product_keyboards(product_id):
    CURRENT_LEVEL = 2

    markup = InlineKeyboardMarkup(row_width=1)
    product = db.select_product(product_id)

    markup.insert(InlineKeyboardButton(text="Xarid qilish", callback_data=buy_cd.new(item_id=product[0])))
    markup.insert(InlineKeyboardButton(text="❌", callback_data=await make_callback_data(CURRENT_LEVEL + 1)))

    return markup

