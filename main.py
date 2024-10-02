from aiogram import Bot, Dispatcher
from asyncio import run, to_thread
from dotenv import load_dotenv
import os
load_dotenv()

bot = Bot(os.getenv('TOKEN'))
dp = Dispatcher()

CURRENCIES = {'RUB': 'руб.', 'RUR': 'руб.', 'KZT': 'тенге', 'EUR': 'евро', 'USD': '$', 'BYR': 'бел. руб.'}
all_vacancies = {}
last_vacancy = {}
all_specialties = []

from core.handlers import commands, reply_text
from core.states import search, main_menu
from core.requestsAPI import get_all_specialties
from core.keyboards import salaries

async def main():
    dp.include_routers(commands.router, reply_text.router, 
                        search.router, main_menu.router)
    response_all_specialties = await get_all_specialties()
    from core.synchronous_functions import create_list_all_specialties
    await to_thread(create_list_all_specialties, response_all_specialties)
    await dp.start_polling(bot)

if __name__ == '__main__':
    run(main())