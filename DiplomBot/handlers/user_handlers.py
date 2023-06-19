from aiogram import Router, F
from aiogram.filters import Command, CommandStart, Text, StateFilter
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message
from keyboards.keyboards import keyboard, nums_keyboard
from lexicon.lexicon import LEXICON_RU
from configdata.config import get_google_sheet_api, get_sheet_data, update_cell_value, number_training, \
    process_sheet_data, get_cell_value
import os
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message
from aiogram.fsm.context import FSMContext

router: Router = Router()


# Определяем состояния для FSM
class CustomProcessStates(StatesGroup):
    wating_for_number = State()
    waiting_for_symbol = State()  # Состояние иожидания ввода символа


# Хандлер который срабатывает на команду start
@router.message(CommandStart(), StateFilter(default_state))
async def process_start_command(message: Message):
    await message.answer(text='Продуктивной тренировки тебе\n\n'
                              'Чтобы посмотреть посещаемость введи или кликни на команду /statistic\n\n'
                              'Чтобы отметить будущих чемпионов тебе понадобиться команда /custom\n\n'
                              'Чтобы отменить выполнение команды нажмите или введите /cancel\n\n'
                              'Хорошего дня и продуктивной тренировки!')


# Хандлер срабатывает на команду /cancel и завершает выбранный процесс если находитесь в нем
@router.message(Command(commands='cancel'), StateFilter(default_state))
async def process_cancel_command(message: Message):
    await message.answer(text='Команда не выбрана, отменять нечего!')


@router.message(Command(commands='cancel'), ~StateFilter(default_state))
async def process_cancel_command_state(message: Message, state: FSMContext):
    await message.answer(text='Вы вышли из выполнения функции')
    await state.clear()


@router.message(Command(commands='custom'))
async def process_custom_commnad(message: Message, state: FSMContext):
    await message.answer(text='Введи номер тренировки от 1 до 9', reply_markup=nums_keyboard)
    await state.set_state(CustomProcessStates.wating_for_number)

@router.callback_query(CustomProcessStates.wating_for_number)
async def process_number_press(callback: CallbackQuery, state: FSMContext):
    number = int(callback.data)
    await state.update_data(number=number)
    await callback.message.answer(text=f'Вы ввели {number}')
    await state.set_state(CustomProcessStates.waiting_for_symbol)


list_sym = ['+', '-', 'o']
@router.message(CustomProcessStates.waiting_for_symbol)
async def process_change_sheet(message: Message, state: FSMContext):
    data = await state.get_data()
    number = data.get('number')
    index = data.get('index', 0)
    name_row = [row[0] for row in get_sheet_data()]
    if index < len(name_row):
        name = name_row[index]
        sym = str(message.text)
        if sym in list_sym:
            await process_sheet_data(number, sym, name, number_training, state)  # Передача всех аргументов
            await message.answer(text=f'Изменено для {name}')
            index += 1  # Увеличение значения индекса
            if index < len(name_row):
                name = name_row[index]
                await message.answer(text=f'Введите символ + - 0 для {name}')
                await state.update_data(index=index)  # Обновление данных состояния
            else:
                await message.answer(text='Ввод символов завершен')
                await state.clear()
        else:
            await message.answer(text='Введены некорректные символы')
    else:
        await message.answer(text='Ввод символов завершен')
        await state.clear()

