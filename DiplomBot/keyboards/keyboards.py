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

button_1: InlineKeyboardButton = InlineKeyboardButton(text='1')
button_2: InlineKeyboardButton = InlineKeyboardButton(text='2')
button_3: InlineKeyboardButton = InlineKeyboardButton(text='3')
button_4: InlineKeyboardButton = InlineKeyboardButton(text='4')
button_5: InlineKeyboardButton = InlineKeyboardButton(text='5')
button_6: InlineKeyboardButton = InlineKeyboardButton(text='6')
button_7: InlineKeyboardButton = InlineKeyboardButton(text='7')
button_8: InlineKeyboardButton = InlineKeyboardButton(text='8')
button_9: InlineKeyboardButton = InlineKeyboardButton(text='9')

nums_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=[[button_1],
                                                                            [button_2],
                                                                            [button_3],
                                                                            [button_4],
                                                                            [button_5],
                                                           [button_6],
                                                           [button_7],
                                                           [button_8],
                                                           [button_9]])
