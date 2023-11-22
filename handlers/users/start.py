from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import ContentType

from keyboards.inline.markups import start
from loader import dp, bot

import io
from reportlab.pdfgen import canvas


@dp.message_handler(commands='start')
async def starting(msg: types.Message, state: FSMContext):
    await msg.answer('Выберите что вы хотите сделать:', reply_markup=start)
    await state.set_state('two_options')


"""1st"""


@dp.callback_query_handler(text='nakladnoy', state='two_options')  # if user wants 1 option
async def first_option(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer('Опишите ваш груз:')
    await call.message.delete()  # deleting to optimize chatting
    await state.set_state('description')  # state for get rid of from some bugs


@dp.message_handler(state='description')
async def description(msg: types.Message, state: FSMContext):
    global desc_of_load
    desc_of_load = msg.text

    await msg.answer('Вес вашего груза(кг):')
    await state.set_state('weight')


@dp.message_handler(state='weight')
async def weight_f(msg: types.Message, state: FSMContext):
    global weight
    weight = msg.text

    await msg.answer('Габариты вашего груза:')
    await state.set_state('dimensions')


@dp.message_handler(state='dimensions')
async def dimensions_f(msg: types.Message, state: FSMContext):
    global dimensions
    dimensions = msg.text

    await msg.answer('Точный адрес отправки:')
    await state.set_state('taking_address')


@dp.message_handler(state='taking_address')
async def taking(msg: types.Message, state: FSMContext):
    global taking_address
    taking_address = msg.text

    await msg.answer('Точный адрес получения:')
    await state.set_state('getting_address')


@dp.message_handler(state='getting_address')
async def getting(msg: types.Message, state: FSMContext):
    global getting_address
    getting_address = msg.text

    await msg.answer('Способ оплаты:')
    await state.set_state('payment')


@dp.message_handler(state='payment')
async def payment(msg: types.Message, state: FSMContext):
    payment = msg.text
    user_id = msg.from_user.id
    pdf_text = \
        f"""Описание груза:
{desc_of_load}
Вес груза:
{weight}
Габариты груза:
{dimensions}
Точный адрес отправки:
{taking_address}
Точный адрес получения:
{getting_address}
Способ оплаты:
{payment}
"""
    pdf_buffer = io.BytesIO()
    pdf = canvas.Canvas(pdf_buffer)
    pdf.drawString(100, 750, pdf_text)
    pdf.save()

    pdf_buffer.seek(0)

    print(pdf_text)
    await bot.send_document(chat_id=user_id, document=types.InputFile(pdf_buffer, filename='test.pdf'))
    await state.set_state('finish1st_option')

"""2nd"""


@dp.callback_query_handler(text='reg_pret', state='two_options')
async def second_option(call: types.Message, state: FSMContext):
    await call.message.answer('Hомер накладной:')
    await state.set_state('number_nak')


@dp.message_handler(state='number_nak')
async def number_nak(msg: types.Message, state: FSMContext):
    await msg.answer('e-mail для ответа на претензию:')
    await state.set_state('email')


@dp.message_handler(state='email')
async def email(msg: types.Message, state: FSMContext):
    await msg.answer('Описание ситуации:')
    await state.set_state('description_situation')


@dp.message_handler(state='description_situation')
async def desc(msg: types.Message, state: FSMContext):
    await msg.answer('Требуемая сумма:')
    await state.set_state('required_amount')


@dp.message_handler(state='required_amount')
async def required_amount(msg: types.Message, state: FSMContext):
    await msg.answer('Фото/Сканы:')
    await state.set_state('photo')


@dp.message_handler(content_types=ContentType.PHOTO, state='photo')
async def photo(msg: types.Message, state: FSMContext):
    await msg.answer('Ваши претензии были сохранены')
    await state.set_state('finish2nd_option')


@dp.message_handler(state='photo')
async def photo_error(msg: types.Message, state: FSMContext):
    await msg.answer('Отправьте фото:')
