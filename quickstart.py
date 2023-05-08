from __future__ import print_function

import os.path
import pickle
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1Q9tONyZayA_oAb6uzxt88OdA4Ba9B3FAtyFc3FKub7k'
SAMPLE_RANGE_NAME = 'May!A17:U33'
# Токен телеграм бота
TOKEN: str = '6224305103:AAGX3MJ1F70glcpS7wXGQGrwkLAaaGRvUMA'
bot: Bot = Bot(TOKEN)
dp: Dispatcher = Dispatcher()

# Файл в который будет сохраняться история запроса
FILENAME = 'user_requests.pkl'
# Создаем словарь в котором будет содержаться список запросов для каждого пользователя
user_requests = {}
# Если файл существует, загружаем из него историю запросов
if os.path.isfile(FILENAME):
    with open(FILENAME, "rb") as file:
        user_requests = pickle.load(file)


# Обработчик команды /history
@dp.message(Command(commands=['history']))
async def process_history_command(message: Message):
    # Получение id пользователя
    user_id = message.from_user.id
    # Проверяем, если пользователь не выполнял еще запросов, то уведомляем его об этом сообщением
    if user_id not in user_requests:
        await message.answer('Вы еще не выполнили ни одного запроса')
        return
    # Вывод сообщений с историей запросов
    requests_user = user_requests[user_id]
    text = 'Ваши запросы:\n' + '\n'.join(requests_user)
    await message.answer(text)


# Обработчик команды /start
@dp.message(Command(commands=['start']))
async def process_start_foo(message: Message):
    """
    Обработчик команды /start
    :param message:
    :return:
    """
    creds = None
    if os.path.exists('../token.json'):
        creds = Credentials.from_authorized_user_file('../token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(r'C:\Users\asics\Desktop\ExcelBOT\credentials.json',
                                                             SCOPES)

            creds = flow.run_local_server(port=0)

        with open('../token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        # Получение данных из таблицы
        service = build('sheets', 'v4', credentials=creds)

        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                    range=SAMPLE_RANGE_NAME).execute()
        values = result.get('values', [])

        # Если данных нет выводит сообщение об их отсутствии
        if not values:
            await message.answer("Данные не обнаружены")
            return

        info_mess = 'Информация о посещаемости и стоимости занятии за месяц для каждого ребенка: \n\n'
        money = {}
        with open(os.path.join(os.path.dirname("C:\\Users\\asics\\Desktop\\ExcelBOT\\start"), 'start.txt'), "w", encoding='utf-8') as start_file:
            for row in values:
                count = 0  # счетчик для подсчета ячеек со значением "(+)"
                for cell in row:
                    if cell == '(+)':
                        count += 1
                start_file.write(f'- {row[1]} - сумма к оплате {count * 400}\n')
        with open('start.txt', 'r', encoding='utf-8') as read_file:
            text = read_file.read()
            await message.answer(text)
    except HttpError as err:
        await message.answer(f'Произошла ошибка: {err}')


# Обработчик команды /help
@dp.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer('Описание команд которые ты можешь выполнить\n'
                         '/start - Выводит список с фамилию, имя ребенка,а так же сумму к оплаты за месяц занятий\n'
                         '/low - Выводит фамилию и имя ребенка с минимальной суммы оплаты за данный месяц\n'
                         '/high - Выводит фамилии и имена детей с максимальной посещаемостью в данном месяце\n'
                         '/custom - вывод показателей пользовательского диапазона\n'
                         '/history - Выводит историю запросов пользователя')


# Обработчик команды /start
@dp.message(Command(commands=['low']))
async def process_start_foo(message: Message):
    """
    Обработчик команды /start
    :param message:
    :return:
    """
    creds = None
    if os.path.exists('../token.json'):
        creds = Credentials.from_authorized_user_file('../token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(r'C:\Users\asics\Desktop\ExcelBOT\credentials.json',
                                                             SCOPES)

            creds = flow.run_local_server(port=0)

        with open('../token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        # Получение данных из таблицы
        service = build('sheets', 'v4', credentials=creds)

        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                    range=SAMPLE_RANGE_NAME).execute()
        values = result.get('values', [])

        # Если данных нет выводит сообщение об их отсутствии
        if not values:
            await message.answer("Данные не обнаружены")
            return
        money = {}
        for row in values:
            count = 0  # счетчик для подсчета ячеек со значением "(+)"
            for cell in row:
                if cell == '(+)':
                    count += 1
            money[row[1]] = count
        sorted_value = sorted(money.values(), reverse=True)
        result_sort = {}
        for i_value in sorted_value:
            for k_value in money.keys():
                if money[k_value] == i_value:
                    result_sort[k_value] = money[k_value]
        with open('low.txt', 'w', encoding='utf-8') as low:
            for k, v in result_sort.items():
                low.write(f'{k} - {v}\n')
        with open('low.txt', 'r', encoding='utf-8') as file:
            text = file.read()
            await message.answer(text)


    except HttpError as err:
        await message.answer(f'Произошла ошибка: {err}')


# Обработчик команды /start
@dp.message(Command(commands=['high']))
async def process_start_foo(message: Message):
    """
    Обработчик команды /start
    :param message:
    :return:
    """
    creds = None
    if os.path.exists('../token.json'):
        creds = Credentials.from_authorized_user_file('../token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(r'C:\Users\asics\Desktop\ExcelBOT\credentials.json',
                                                             SCOPES)

            creds = flow.run_local_server(port=0)

        with open('../token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        # Получение данных из таблицы
        service = build('sheets', 'v4', credentials=creds)

        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                    range=SAMPLE_RANGE_NAME).execute()
        values = result.get('values', [])

        # Если данных нет выводит сообщение об их отсутствии
        if not values:
            await message.answer("Данные не обнаружены")
            return
        money = {}
        for row in values:
            count = 0  # счетчик для подсчета ячеек со значением "(+)"
            for cell in row:
                if cell == '(+)':
                    count += 1
            money[row[1]] = count
        sorted_value = sorted(money.keys())
        result_sort = {}
        for i_value in sorted_value:
            for k_value in money.keys():
                if money[k_value] == i_value:
                    result_sort[k_value] = money[k_value]
        with open('high.txt', 'w', encoding='utf-8') as high:
            for k, v in result_sort.items():
                high.write(f'{k} - {v}\n')
        with open('high.txt', 'r', encoding='utf-8') as file:
            text = file.read()
            await message.answer(text)


    except HttpError as err:
        await message.answer(f'Произошла ошибка: {err}')


# Обработчик всех остальных сообщений
@dp.message()
async def other_message(message: Message):
    user_id = message.from_user.id
    text = message.text
    if user_id not in user_requests:
        user_requests[user_id] = []
    user_requests[user_id].append(text)

    with open(FILENAME, 'w+') as f:
        pickle.dump(user_requests, f)

if __name__ == '__main__':
    dp.run_polling(bot)
