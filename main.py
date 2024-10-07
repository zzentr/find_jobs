from aiogram import Bot, Dispatcher
from asyncio import run, to_thread
from dotenv import load_dotenv
import os
load_dotenv()

bot = Bot(os.getenv('TOKEN'))
dp = Dispatcher()

POPULAR_CITIES = ['Москва', 'Санкт-Петербург', 'Владивосток', 'Екатеринбург', 'Воронеж', 'Краснодар', 'Сочи',
                'Калуга', 'Казань', 'Новосибирск', 'Красноярск', 'Пермь', 'Самара', 'Саратов', 'Уфа', 
                'Ярославль', 'Ростов-на-Дону', 'Нижний Новгород']
CURRENCIES = {'RUB': 'руб.', 'RUR': 'руб.', 'KZT': 'тенге', 'EUR': 'евро', 'USD': '$', 'BYR': 'бел. руб.',
               'UZS': 'узбек. сум', 'AZN': 'манат', 'GEL': 'грузин. лари', 'UAH': 'гривн'}
EXPERIENCE = {
      'Нет опыта': 'noExperience',
      'От 1 года до 3 лет': 'between1And3',
      'От 3 до 6 лет': 'between3And6',
      'Более 6 лет': 'moreThan6'
}
EMPLOYMENT = {
    'Полная занятость': 'full',
    'Частичная занятость': 'part',
    'Волонтерство': 'volunteer',
    'Стажировка': 'probation'
}
SCHEDULE = {
    'Полный день': 'fullDay',
    'Сменный график': 'shift',
    'Гибкий график': 'flexible',
    'Удаленная работа': 'remote'
}
all_vacancies = {}
last_vacancy = {}
all_specialties = []
all_areas = {}

from core.handlers import commands
from core.handlers.states import search, main_menu
from core.requestsAPI import get_all_specialties, get_all_areas

async def main():
    dp.include_routers(commands.router, search.router, main_menu.router)
    response_all_specialties = await get_all_specialties()
    respons_all_areas = await get_all_areas()
    from core.synchronous_functions import create_list_all_specialties, create_dict_all_areas
    await to_thread(create_list_all_specialties, response_all_specialties)
    await to_thread(create_dict_all_areas, respons_all_areas)
    await dp.start_polling(bot)

if __name__ == '__main__':
    run(main())