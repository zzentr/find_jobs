from asyncio import to_thread
from re import fullmatch, findall

from main import all_specialties, all_vacancies, id_posted_vacancies
from core.handlers.states.imports import *
from core.requestsAPI import get_vacancies, get_one_vacancy
from core.keyboards import more_vacancies, specialties, salaries, areas
from core.synchronous_functions import create_dict_with_vacancies, create_message_one_vacancy, check_correct_area

router = Router()


class Vacancies(StatesGroup):

    speciality = State()
    salary = State()
    area = State()
    show_vacancies = State()


@router.message(Vacancies.speciality)
async def choose_speciality(message: Message, state: FSMContext):
    """Проверяем специальность и отправляем зарплаты"""
    speciality = message.text

    if speciality.lower() not in (spec.lower() for spec in all_specialties):
        await message.answer('Введите корректную специальность')
        return

    await state.update_data(speciality=speciality)
    await state.set_state(Vacancies.salary)
    await message.answer('Выберите желаемую заработную плату\nЕсли она не важна нажмите на \"Пропустить"',
                          reply_markup=await salaries(speciality))

@router.message(Vacancies.salary)
async def choose_salary(message: Message, state: FSMContext):
    """Проверяем зарплату и оправляем регион"""
    salary = message.text

    if salary == '⇐ Специальность':
        await state.set_state(Vacancies.speciality)
        await message.answer('Выберите специальность по которой нужно найти вакансии или напишите сами',
                          reply_markup=await specialties(message.from_user.id, True))
        return

    if fullmatch(r'от \d* ₽', salary) or fullmatch(r'\d+', salary) or fullmatch(r'\d+ ₽', salary) or fullmatch(r'от \d+', salary):
        salary = int(findall(r'\d+', salary)[0])
    
    if type(salary) != int or salary <= 0:
            await message.answer('Выберите желаемую заработную плату\nЕсли она не важна то нажмите на \"Пропустить"')
            return
    
    await state.update_data(salary=salary)
    await state.set_state(Vacancies.area)
    await message.answer('Выберите город в котором нужно найти вакансии или напишите сами',
                         reply_markup=await areas(message.from_user.id, True))

@router.message(Vacancies.area)
async def choose_area(message: Message, state: FSMContext):
    """Проверяем регион и отправляем список вакансий по этим фильтрам"""
    area = message.text.lower()
    
    if area == '⇐ зарплата':
         speciality = await state.get_data()
         await state.set_state(Vacancies.salary)
         await message.answer('Выберите желаемую заработную плату\nЕсли она не важна нажмите на \"Пропустить"',
                            reply_markup=await salaries(speciality['speciality']))
         return

    id_area = await to_thread(check_correct_area, area)

    if not id_area:
        await message.answer('Выберите город в котором нужно найти вакансии или напишите сами')
        return
    
    await state.update_data(area=id_area)
    await state.set_state(Vacancies.show_vacancies)

    data = await state.get_data()
    response = await get_vacancies(data['speciality'], data['area'], data['salary'])
    vacancies = response['items']

    message_vacancies = await to_thread(create_dict_with_vacancies, vacancies, message.from_user.id)
    await message.answer(message_vacancies, parse_mode='html', reply_markup=more_vacancies, disable_web_page_preview=True)

@router.message(Vacancies.show_vacancies)
async def send_more_vacancies(message: Message, state: FSMContext):
    """Выводим подробную информацию про одну вакансию"""
    number_vacancy = message.text
    tg_id = message.from_user.id

    if not fullmatch(r'\d+', number_vacancy) or not id_posted_vacancies.get(int(number_vacancy)):
        print(fullmatch(r'\d+', number_vacancy))
        print(id_posted_vacancies.get(number_vacancy))
        await message.answer('Напишите мне номер вакансии или выберите действие на клавиатуре, например, уточнить фильтры')
        return
    
    id_vacancy = all_vacancies[tg_id][int(number_vacancy)]['id']
    response = await get_one_vacancy(id_vacancy)
    message_one_vacancy = await to_thread(create_message_one_vacancy, response)

    await message.answer(message_one_vacancy, parse_mode='html')