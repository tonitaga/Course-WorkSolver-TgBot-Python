from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           ReplyKeyboardMarkup)

from bot.serveces.payment import get_quickpay_form


def get_kb(*args) -> ReplyKeyboardMarkup:
    """Creates a keyboard with buttons in a column"""
    kb = ReplyKeyboardMarkup(resize_keyboard=True)

    for button_name in args:
        kb.add(button_name)

    return kb


def get_ikb(callback_data: list, label: str, service_type: str) -> InlineKeyboardMarkup:
    """Creates inline keyboard with buttons in a column"""
    ikb = InlineKeyboardMarkup(row_width=1)

    ib1 = InlineKeyboardButton("✅ Все верно! Рассчитать",
                               callback_data=callback_data[0],
                               )
    ib2 = InlineKeyboardButton("❌ Переписать значения", callback_data=callback_data[1])
    ib3 = InlineKeyboardButton(f"💵 Оплатить {300 if service_type == 'cutter' else 400} руб",
                               url=get_quickpay_form(label, service_type).redirected_url
                               )

    ikb.add(ib1).add(ib2).add(ib3)
    return ikb
