from asyncio import to_thread
from re import fullmatch, findall

from main import all_specialties
from core.states.imports import *
from core.requestsAPI import get_vacancies
from core.keyboards import more_vacancies, salaries, areas
from core.synchronous_functions import create_dict_with_vacancies

router = Router()


class Vacancies(StatesGroup):

    speciality = State()
    salary = State()
    area = State()
    show_vacancies = State()


@router.message(Vacancies.speciality)
async def choose_speciality(message: Message, state: FSMContext):
    speciality = message.text

    if speciality not in all_specialties:
        await message.answer('Введите корректную специальность')
        return

    await state.set_data(data={'speciality':speciality})
    await state.set_state(Vacancies.salary)
    await message.answer('Выберите желаемую заработную плату\nЕсли она не важна нажмите на \"Пропустить"',
                          reply_markup=await salaries(speciality))

@router.message(Vacancies.salary)
async def choose_salary(message: Message, state: FSMContext):
    salary = message.text

    if fullmatch(r'от \d* ₽', salary):
        salary = findall(r'\d+', salary)[0]
    
    elif fullmatch(r'\d+', salary) or fullmatch(r'\d+ ₽', salary) or fullmatch(r'от \d+', salary):
        salary = findall(r'\d+', salary)[0]
    
    else: 
        await message.answer('Выберите желаемую заработную плату\nЕсли она не важна то нажмите на \"Пропустить"')
        return
    
    await state.set_data(data={'salary':salary})
    await state.set_state(Vacancies.area)
    speciality = await state.get_data()
    print(speciality['speciality'])
    # await message.answer('Выберите город в котором нужно найти вакансии или напишите сами', reply_markup=await areas(speciality))

async def send_vacancies(message: Message, state: FSMContext):
    speciality = message.text
    response = await get_vacancies(speciality)
    vacancies = response['items']
    message_vacancies = await to_thread(create_dict_with_vacancies, vacancies, message.from_user.id)
    await message.answer(message_vacancies, parse_mode='html', reply_markup=more_vacancies, disable_web_page_preview=True)
    await state.clear()
