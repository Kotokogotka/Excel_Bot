from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from lexicon.lexicon import LEXICON_RU
from configdata.config import number_training


button_1: InlineKeyboardButton = InlineKeyboardButton(text='1', callback_data='1')
button_2: InlineKeyboardButton = InlineKeyboardButton(text='2', callback_data='2')
button_3: InlineKeyboardButton = InlineKeyboardButton(text='3', callback_data='3')
button_4: InlineKeyboardButton = InlineKeyboardButton(text='4', callback_data='4')
button_5: InlineKeyboardButton = InlineKeyboardButton(text='5', callback_data='5')
button_6: InlineKeyboardButton = InlineKeyboardButton(text='6', callback_data='6')
button_7: InlineKeyboardButton = InlineKeyboardButton(text='7', callback_data='7')
button_8: InlineKeyboardButton = InlineKeyboardButton(text='8', callback_data='8')
button_9: InlineKeyboardButton = InlineKeyboardButton(text='9', callback_data='9')

nums_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(
    inline_keyboard=[[button_1],
                     [button_2],
                     [button_3],
                     [button_4],
                     [button_5],
                     [button_6],
                     [button_7],
                     [button_8],
                     [button_9]])



button_1: KeyboardButton = KeyboardButton(text=LEXICON_RU['plus'])
button_2: KeyboardButton = KeyboardButton(text=LEXICON_RU['minus'])
button_3: KeyboardButton = KeyboardButton(text=LEXICON_RU['absent'])


sym_kb: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
                                    keyboard=[[button_1],
                                              [button_2],
                                              [button_3]],
                                    resize_keyboard=True, one_time_keyboard=True)
