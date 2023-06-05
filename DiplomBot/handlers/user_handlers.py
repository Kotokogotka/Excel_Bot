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

# Хандлер срабатывает на команду/custom
@router.message(Command(commands=['/custom']))
async def process_custom_command(message: Message):
    for name in get_google_sheet_api()



