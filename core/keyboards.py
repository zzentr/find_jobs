from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from main import all_specialties, POPULAR_CITIES
from core.requestsAPI import get_salary_for_speciality

last_speciality_show = {}
last_city_show = {}

main_menu = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Искать вакансии')],
                                        [KeyboardButton(text='что-то')]],
                                resize_keyboard=True)
more_vacancies = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Ещё ⇒')],
                                               [KeyboardButton(text='Уточнить параметры поиска')],
                                               [KeyboardButton(text='Главное меню')]],
                                      resize_keyboard=True)

additional_options = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Вернуться к поиску')],
                                                   [KeyboardButton(text='Главное меню')]])

experiences = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Нет опыта'), KeyboardButton(text='От 1 года до 3 лет')],
                                            [KeyboardButton(text='От 3 до 6 лет'), KeyboardButton(text='Более 6 лет')],
                                            [KeyboardButton(text='Главное меню')]])

employments = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Полная занятость'), KeyboardButton(text='Частичная занятость')],
                                            [KeyboardButton(text='Волонтерство'), KeyboardButton(text='Стажировка')],
                                            [KeyboardButton(text='Главное меню')]])

schedules = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Полный день'), KeyboardButton(text='Сменный график')],
                                            [KeyboardButton(text='Гибкий график'), KeyboardButton(text='Удаленная работа')],
                                            [KeyboardButton(text='Главное меню')]])

async def specialties(tg_id, keyboard_reset=False):
    global last_speciality_show
    keyboboard = ReplyKeyboardBuilder()
    if not last_speciality_show.get(tg_id):
        last_speciality_show[tg_id] = 0

    if keyboard_reset:
        last_speciality_show[tg_id] = 0
    
    to = last_speciality_show[tg_id] + 6
    last_index = False

    for speciality in all_specialties[last_speciality_show[tg_id]:to]:
        keyboboard.add(KeyboardButton(text=speciality))
        if speciality == all_specialties[-1]:
            last_index = True

    keyboboard.adjust(2)
    if last_speciality_show[tg_id] != 0 and not last_index:
        keyboboard.row(KeyboardButton(text='⇐ Назад'), KeyboardButton(text='Ещё ⇒'))
    elif last_index:
        keyboboard.row(KeyboardButton(text='⇐ Назад'))
    else:
        keyboboard.row(KeyboardButton(text='Ещё ⇒'))
    keyboboard.row(KeyboardButton(text='Главное меню'))

    if not last_index:
        last_speciality_show[tg_id] = to

    return keyboboard.as_markup(resize_keyboard=True)

async def salaries(speciality: str, update_data=False):
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
    if not update_data:
        keyboard.row(KeyboardButton(text='⇐ Специальность'))
    keyboard.row(KeyboardButton(text='Пропустить'))
    keyboard.row(KeyboardButton(text='Главное меню'))

    return keyboard.as_markup(resize_keyboard=True)

async def areas(tg_id, keyboard_reset=False, update_data=False):
    global last_city_show
    keyboboard = ReplyKeyboardBuilder()
    if not last_city_show.get(tg_id):
        last_city_show[tg_id] = 0

    if keyboard_reset:
        last_city_show[tg_id] = 0
    
    to = last_city_show[tg_id] + 6

    for city in POPULAR_CITIES[last_city_show[tg_id]:to]:
        keyboboard.add(KeyboardButton(text=city))

    keyboboard.adjust(2)
    if last_city_show[tg_id] not in (0, 12):
        keyboboard.row(KeyboardButton(text='⇐ Назад'), KeyboardButton(text='Ещё ⇒'))
    elif last_city_show[tg_id] == 12:
        keyboboard.row(KeyboardButton(text='⇐ Назад'))
    else:
        keyboboard.row(KeyboardButton(text='Ещё ⇒'))
        
    if not update_data:
        keyboboard.row(KeyboardButton(text='⇐ Зарплата'))
    keyboboard.row(KeyboardButton(text='Пропустить'))
    keyboboard.row(KeyboardButton(text='Главное меню'))

    if last_city_show[tg_id] != 12:
        last_city_show[tg_id] = to

    return keyboboard.as_markup(resize_keyboard=True)