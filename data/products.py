from aiogram import types
from aiogram.types import LabeledPrice

from utils.misc.product import Product


def create_product_invoice(product: list):
    item = Product(
        title=f"{product[1]} ni sotib olish",
        description=product[2],
        currency="UZS",
        prices=[
            LabeledPrice(
                label=f"{product[1]}",
                amount=int(product[3] * 1213411)
            ),
            LabeledPrice(
                label="Yetkazib berish (7 kun)",
                amount=1500000
            )
        ],
        start_parameter=f"product_id_start",
        photo_url=product[4],
        photo_width=1200,
        photo_height=703,
        need_email=True,
        need_name=True,
        need_phone_number=True,
        need_shipping_address=True,
        is_flexible=True
    )
    return item


REGULAR_EXPRESS = types.ShippingOption(
    id='regular',
    title="Regular Express",
    prices=[
        LabeledPrice(
            label='Fargo (3 kun)',
            amount=1500000
        ),
    ]
)

FAST_EXPRESS = types.ShippingOption(
    id='fast',
    title="Fast Express",
    prices=[
        LabeledPrice(
            label='Tez yetkazib berish (1 kun)',
            amount=2500000
        ),
    ]
)

PICKUP_EXPRESS = types.ShippingOption(
    id='pickup',
    title="Pickup Express",
    prices=[
        LabeledPrice(
            label='Do\'kondan olib ketish',
            amount=-1500000
        ),
    ]
)
