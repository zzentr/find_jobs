from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from main import all_specialties
from core.requestsAPI import get_salary_for_speciality

last_speciality_show = {}

main_menu = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Искать вакансии')],
                                        [KeyboardButton(text='что-то')]],
                                resize_keyboard=True)
more_vacancies = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Показать ещё')]], resize_keyboard=True)

async def specialties(tg_id):
    global last_speciality_show
    keyboboard = ReplyKeyboardBuilder()
    if not last_speciality_show.get(tg_id):
        last_speciality_show[tg_id] = 0
    
    to = last_speciality_show[tg_id] + 6

    for speciality in all_specialties[last_speciality_show[tg_id]:to]:
        keyboboard.add(KeyboardButton(text=speciality))

    keyboboard.adjust(2)
    keyboboard.row(KeyboardButton(text='Показать ещё'))
    keyboboard.row(KeyboardButton(text='Главное меню'))

    return keyboboard.as_markup(resize_keyboard=True)

async def salaries(speciality: str):
    keyboard = ReplyKeyboardBuilder()
    response = await get_salary_for_speciality(speciality)
    salaries = response['clusters'][1]
    
    for i, salary_name in enumerate(salaries['items']):
        salary = salary_name['name']
        if i == 5:
            break
        if salary == 'Указан':
            continue

        keyboard.add(KeyboardButton(text=salary))
    
    keyboard.adjust(2)
    keyboard.row(KeyboardButton(text='Пропустить'), KeyboardButton(text='Назад'), KeyboardButton(text='Главное меню'))

    return keyboard.as_markup(resize_keyboard=True)

async def areas():
    pass