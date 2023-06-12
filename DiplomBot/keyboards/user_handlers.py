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


# Хандлер срабатывает на команду custom и переводит бота в состояние ожидания ввода номера тренировки
@router.message(Command(commands='custom'), StateFilter(default_state))
async def process_custom_command(message: Message, state: FSMContext):
    await message.answer(text='Введите номер тренировки')
    # Устанавливаем состояние ожидания ввода
    await state.set_state(CustomProcessStates.wating_for_number)


# Хандлер срабатывает если введено корректное значение от 1 до 9
# Ожидает ввода символа
@router.message(StateFilter(CustomProcessStates.wating_for_number),
                lambda x: x.text.isdigit() and 1 <= int(x.text) <= 9)
async def process_number_input(message: Message, state: FSMContext):
    await state.update_data(number=message.text)
    await message.answer(text='Принял, теперь вводим отметку + - О для каждого ребенка')
    await state.set_state(CustomProcessStates.waiting_for_symbol)


# Хандлер срабатывает если введено некорректное значение номера тренировки
@router.message(StateFilter(CustomProcessStates.wating_for_number))
async def process_warning_number(message: Message):
    await message.answer(text='Введено не корректное значение, введите цифру от 1 до 9\n\n'
                              'Если хотите отменить команду, отправьте /cancel')


# Хандлер срабатывает если введен корректный
sym_list = ['+', '-', 'O', 'o', 'о', 'О']
@router.message(StateFilter(CustomProcessStates.waiting_for_symbol),
                lambda sym: sym.text.isalpha() and sym in sym_list)
async def process_symbol_input(message: Message, state: FSMContext):
    # Сохраняю символ в хранилище по ключу symbol
    await state.update_data(sym=message.text)
    # Создаю объект инлайн кнопок + -
    plus = InlineKeyboardButton(text='Присутсвовал',
                                callback_data='+')
    minus = InlineKeyboardButton(text='Отсутсвует',
                                 callback_data='-')
    good_reason = InlineKeyboardButton(text='Не смог присутсвовать',
                                       callback_data='O')
    # Добавляем кнопки в клавиатуру
    sym_keyboard: list[list[InlineKeyboardButton]] = [[plus, minus, good_reason]]
    # Создаем объект инлайн клавиатуры
    markup = InlineKeyboardMarkup(inline_keyboard=sym_keyboard)
    await message.answer(text='Выберете действие для {name}', reply_markup=markup)
