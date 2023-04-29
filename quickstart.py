from __future__ import print_function

import os.path

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

TOKEN: str = '6222646713:AAGDt8fxG7EG7bNAwdX4uj6hi4r_-r9spNA'
bot: Bot = Bot(TOKEN)
dp: Dispatcher = Dispatcher()


@dp.message(Command(commands=['start']))
async def process_start_foo(message: Message):
    """
    Обработчик команды /start
    :param message:
    :return:
    """
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token.json', 'w') as token:
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
        for row in values:
            count = 0  # счетчик для подсчета ячеек со значением "(+)"
            for cell in row:
                if cell == '(+)':
                    count += 1
            money[row[1]] = count
        await message.answer(info_mess)
        for k, v in money.items():
            await message.answer(f'Имя {k} - Сумма к оплате {v} рублей')
    except HttpError as err:
        await message.answer(f'Произошла ошибка: {err}')


@dp.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer('Описание команд которые ты можешь выполнить\n'
                         '/start - Выводит список с фамилию, имя ребенка,а так же сумму к оплаты за месяц занятий\n'
                         '/low - Выводит фамилию и имя ребенка с минимальной суммы оплаты за данный месяц\n'
                         '/high - Выводит фамилии и имена детей с максимальной посещаемостью в данном месяце\n'
                         '/custom - вывод показателей пользовательского диапазона\n'
                         '/history - Выводит историю запросов пользователя')

if __name__ == '__main__':
    dp.run_polling(bot)
