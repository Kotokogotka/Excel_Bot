from aiogram import Router
from aiogram.filters import Command, CommandStart, Text
from aiogram.types import Message
from keyboards.keyboards import keyboard
from lexicon.lexicon import LEXICON_RU
from configdata.config import get_google_sheet_api, get_sheet_data, update_sheet_data

import os

router: Router = Router()


# Данный хандлер срабатывает на команду /start
@router.message(CommandStart())
async def process_start_command(message: Message):
    get_google_sheet_api()
    await message.answer(text=LEXICON_RU['/start'],
                         reply_markup=keyboard)
    with open(os.path.join(os.path.dirname("C:\\Users\\asics\\Desktop\\AtlantBot\\handlers\\start.txt"), 'start.txt'),
              "w",
              encoding='utf-8') as start_file:
        for row in get_sheet_data():
            count = 0  # счетчик для подсчета ячеек со значением "(+)"
            for cell in row:
                if cell == '(+)':
                    count += 1
            start_file.write(f'- {row[1]} - количество посещений {count}\n')
    with open('C:\\Users\\asics\\Desktop\\AtlantBot\\handlers\\start.txt', 'r', encoding='utf-8') as read_file:
        text = read_file.read()
        await message.answer(text)


# Хандлер срабатывает на команду /help
@router.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer(text=LEXICON_RU['/help'])


# Хандлер срабатывает на нажатие на любую кнопку из пердложеных вариантов
@router.message(Text(text=[LEXICON_RU['+'],
                           LEXICON_RU['-'],
                           LEXICON_RU['O']]))
async def process_choice_button(message: Message):
    await message.answer(text='Выберите действие')

@router.message(Command(commands=['custom']))
async def process_custom_process(message: Message, state: FSMContext):
    await state.set_state('waiting_for_training_number')  # Установка состояния ожидания ввода номера тренировки
    await message.answer('Выберите номер тренировки', reply_markup=nums_keyboard)
    





@router.callback_query(lambda c: c.data == '1')
async def process_callback_one(callback_query: CallbackQuery, state: FSMContext):
    # Получаем номер тренировки из колбека
    training_number = 1

    # Получаем символ из состояния FSMContext
    symbol = await state.get_state()

    # Вызываем функцию process_sheet_data
    process_sheet_data(training_number, symbol)

    # Отправляем ответ пользователю
    await callback_query.answer('Действия успешно выполнены')

@router.callback_query(lambda c: c.data == '2')
async def process_callback_one(callback_query: CallbackQuery, state: FSMContext):
    # Получаем номер тренировки из колбека
    training_number = 2

    # Получаем символ из состояния FSMContext
    symbol = await state.get_state()

    # Проверяем, что символ не является None, чтобы избежать нежелательного заполнения таблицы
    if symbol is not None:
        # Вызываем функцию process_sheet_data
        process_sheet_data(training_number, symbol)

        # Отправляем ответ пользователю
        await callback_query.answer('Действия успешно выполнены')
    else:
        # Если символ None, выводим сообщение об ошибке
        await callback_query.answer('Ошибка: символ не выбран')

