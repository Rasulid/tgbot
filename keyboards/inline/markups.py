from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types.web_app_info import WebAppInfo


start = InlineKeyboardMarkup(
    inline_keyboard=[
    [
        InlineKeyboardButton(text='Создать накладной',callback_data='nakladnoy')
    ],
    [
        InlineKeyboardButton(text='Регистрация претензии', callback_data='reg_pret')
    ]
])