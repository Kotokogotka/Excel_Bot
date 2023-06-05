from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from lexicon.lexicon import LEXICON_RU

# Создаем объект с кнопками
button_plus: InlineKeyboardButton = InlineKeyboardButton(text=LEXICON_RU['+'])
button_minus: InlineKeyboardButton = InlineKeyboardButton(text=LEXICON_RU['-'])
button_absent: InlineKeyboardButton = InlineKeyboardButton(text=LEXICON_RU['O'])

# Инициализируем клавиатуру с кнопками
my_kb: ReplyKeyboardBuilder = ReplyKeyboardBuilder()

# Добавляем кнопки в билдер с параметром width=3
my_kb.row(button_plus, button_minus, button_absent, width=3)

# Создаем клавиатуру с кнопками + - О
keyboard = my_kb.as_markup(one_time_keyboard=True, resize_keyboard=True)
