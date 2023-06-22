from aiogram import Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.state import default_state
from keyboards.keyboards import sym_kb, nums_keyboard
from configdata.config import get_google_sheet_api, get_sheet_data, process_sheet_data, number_training
import os
from aiogram.types import CallbackQuery, Message
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


# Хандлер срабатывает на команду statistic выводя информацию о посещаемости
@router.message(Command(commands='statistic'))
async def process_statistic_command(message: Message):
    get_google_sheet_api()
    with open(os.path.join(os.path.dirname("C:\\Users\\asics\\Desktop\\AtlantBot\\handlers\\start.txt"), 'start.txt'),
              "w",
              encoding='utf-8') as start_file:
        for row in get_sheet_data():
            count = 0  # счетчик для подсчета ячеек со значением "(+)"
            for cell in row:
                if cell == '+':
                    count += 1
            start_file.write(f'- {row[0]} - количество посещений {count}\n')
    with open('C:\\Users\\asics\\Desktop\\AtlantBot\\handlers\\start.txt', 'r', encoding='utf-8') as read_file:
        text = read_file.read()
        await message.answer(text)


# Хандлер срабатывает на команду /cancel и завершает выбранный процесс если находитесь в нем
@router.message(Command(commands='cancel'), StateFilter(default_state))
async def process_cancel_command(message: Message):
    await message.answer(text='Команда не выбрана, отменять нечего!')

# Хандлер срабатывает на команду /cancel если пользователь находится вне выполнения функции
@router.message(Command(commands='cancel'), ~StateFilter(default_state))
async def process_cancel_command_state(message: Message, state: FSMContext):
    await message.answer(text='Вы вышли из выполнения функции')
    await state.clear()

# Хандлер срабатывает на функцию custom и запускается процесс выбора номера тренировки и дальнейшей отметки в таблице
@router.message(Command(commands='custom'))
async def process_custom_commnad(message: Message, state: FSMContext):
    await message.answer(text='Введи номер тренировки от 1 до 9', reply_markup=nums_keyboard)
    await state.set_state(CustomProcessStates.wating_for_number)


# Cрабатывает на нажатие кнопки инлайн клавиатуры и переходит в состояние ожидания ввода символа
@router.callback_query(CustomProcessStates.wating_for_number)
async def process_number_press(callback: CallbackQuery, state: FSMContext):
    number = int(callback.data)
    await state.update_data(number=number)
    await callback.message.answer(text=f'Вы ввели {number}')
    await state.set_state(CustomProcessStates.waiting_for_symbol)

# Cписок допустимых символов если пользователь не захочет выполнить ввод с кнопки, а в ручную
list_sym = ['+', '-', 'o']


# Функция в которой запускается после ввода номера тренировки.
# Выполняется ввод символов для каждого ребенка и заноситься в соответственную клетку
@router.message(CustomProcessStates.waiting_for_symbol)
async def process_change_sheet(message: Message, state: FSMContext):
    data = await state.get_data()
    number = data.get('number')
    index = data.get('index', 0)
    name_row = [row[0] for row in get_sheet_data()]
    if index < len(name_row):
        name = name_row[index]
        if index == 0:
            await message.answer(text=f'Введите символ + - 0 для {name}', reply_markup=sym_kb)
        sym = str(message.text)
        if sym in list_sym:
            await process_sheet_data(number, sym, name, number_training, state)
            await message.answer(text=f'Изменено для {name}')
            index += 1
            if index < len(name_row):
                name = name_row[index]
                await message.answer(text=f'Введите символ + - 0 для {name}', reply_markup=sym_kb)
                await state.update_data(index=index)
            else:
                await message.answer(text='Ввод символов завершен')
                await state.clear()
        else:
            await message.answer(text='Введены некорректные символы')
    else:
        await message.answer(text='Ввод символов завершен')
        await state.clear()

