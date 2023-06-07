from __future__ import print_function

from googleapiclient.discovery import build
from dataclasses import dataclass
from environs import Env
import os
import pickle
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from aiogram import Router
import googleapiclient.discovery


@dataclass
class TgBot:
    token: str  # Токен для доступа к телеграм боту


@dataclass
class Config:
    tg_bot: TgBot


def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(tg_bot=TgBot(token=env("BOT_TOKEN")))


router: Router = Router()

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SAMPLE_SPREADSHEET_ID = '1Q9tONyZayA_oAb6uzxt88OdA4Ba9B3FAtyFc3FKub7k'
SAMPLE_RANGE_NAME = 'May!B17:Z39'


def get_google_sheet_api():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                r'C:\Users\asics\Desktop\AtlantBot\configdata\credentials.json',
                SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    service = googleapiclient.discovery.build('sheets', 'v4', credentials=creds)
    return service.spreadsheets()


def get_cell_value(cell):
    service = get_google_sheet_api()
    result = service.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                  range=cell).execute()
    values = result.get('values', [])
    if values:
        return values[0][0]
    else:
        return None


def update_cell_value(cell, symbol):
    service = get_google_sheet_api()
    body = {
        'values': [
            [symbol]
        ]
    }
    service.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                            range=cell,
                            valueInputOption='RAW',
                            body=body).execute()


def get_sheet_data():
    service = get_google_sheet_api()
    result = service.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                  range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])
    return values



def process_sheet_data(training, symbol, number_training):
    values = get_sheet_data()
    name_row = [row[0] for row in values]
    cnt = 0
    for name in name_row:
        index = None
        for i, row in enumerate(values):
            if row and row[0] == name:
                index = i
                break
        if index is not None:
            cell = f'{number_training[training]}{17 + cnt}'
            update_cell_value(cell, symbol)
            cnt += 1
        else:
            print(f'Ошибка: Значение {name} не найдено в таблице.')
