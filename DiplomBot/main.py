import asyncio
import logging

from aiogram import Bot, Dispatcher
from configdata.config import Config, load_config
from handlers import user_handlers
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand

# Инициализируем логгер
logger = logging.getLogger(__name__)

# Функция конфигурирования и запуска бота
async def main():
    # Конфигурирование логирование
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')

    # Вывод в консоль информацию о запуске бота
    logger.info('Бот запущен!')

    # Загружаем конфиг в переменную config
    config: Config = load_config()

    # Инициализация бота и диспатчера
    bot: Bot = Bot(token=config.tg_bot.token,
                   parse_mode='HTML')
    storage = MemoryStorage()
    dp: Dispatcher = Dispatcher(storage=storage)

    # Региистрация роутера в диспатчере
    dp.include_router(user_handlers.router)

    main_menu_commands = [
        BotCommand(command='/help',
                   description='Справка о работе бота'),
        BotCommand(command='/start',
                   description='Запуск бота'),
        BotCommand(command='/statistic',
                   description='Узнать посещаемость'),
        BotCommand(command='/custom',
                   description='Отметить детей'),
        BotCommand(command='cancel',
                   description='Прервать действие')]

    # Установка меню
    await bot.set_my_commands(main_menu_commands)
    # Пропускаем апдейты и запускаем пулинг
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
