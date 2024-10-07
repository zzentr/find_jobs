from asyncio import to_thread
from re import fullmatch, findall

from main import EXPERIENCE, EMPLOYMENT, SCHEDULE, all_specialties
from core.handlers.states.imports import *
from core.requestsAPI import get_vacancies
from core.keyboards import (more_vacancies, additional_options, experiences, employments, schedules,
                            specialties, salaries, areas)
from core.synchronous_functions import (create_dict_with_vacancies, check_correct_area, create_message_with_selected_options)

router = Router()


class Vacancies(StatesGroup):

    speciality = State()
    salary = State()
    area = State()
    experience = State()
    employment = State()
    schedule = State()
    show_vacancies = State()
    additional_options = State()


@router.message(Vacancies.speciality)
async def choose_speciality(message: Message, state: FSMContext):
    """Проверяем специальность и отправляем зарплаты"""
    speciality = message.text

    if speciality.lower() not in (spec.lower() for spec in all_specialties):
        await message.answer('Введите корректную специальность')
        return

    await state.update_data(speciality=speciality)
    data = await state.get_data()
    if data.get('update_data'):
        await state.update_data(update_data=None)
        await send_message_with_choose_options(message, state)
        return
    
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
    
    if salary == 'Пропустить':
        salary = None

    else:
        if fullmatch(r'от \d* ₽', salary) or fullmatch(r'\d+', salary) or fullmatch(r'\d+ ₽', salary) or fullmatch(r'от \d+', salary):
            salary = int(findall(r'\d+', salary)[0])
    
        if type(salary) != int or salary <= 0:
            await message.answer('Выберите желаемую заработную плату\nЕсли она не важна то нажмите на \"Пропустить"')
            return
    
    await state.update_data(salary=salary)
    data = await state.get_data()
    if data.get('update_data'):
        await state.update_data(update_data=None)
        await send_message_with_choose_options(message, state)
        return
    
    await state.set_state(Vacancies.area)
    await message.answer('Выберите город в котором нужно найти вакансии или напишите сами',
                         reply_markup=await areas(message.from_user.id, True))

@router.message(Vacancies.area)
async def choose_area(message: Message, state: FSMContext):
    """Проверяем регион и отправляем список вакансий по этим фильтрам"""
    area = message.text
    
    if area == '⇐ Зарплата':
         speciality = await state.get_data()
         await state.set_state(Vacancies.salary)
         await message.answer('Выберите желаемую заработную плату\nЕсли она не важна нажмите на \"Пропустить"',
                            reply_markup=await salaries(speciality['speciality']))
         return
    
    if area == 'Пропустить':
        await state.update_data(area=None)

    else:
        id_area = await to_thread(check_correct_area, area.lower())

        if not id_area:
            await message.answer('Выберите город в котором нужно найти вакансии или напишите сами')
            return
        await state.update_data(area=[id_area, area])
    
    data = await state.get_data()
    if data.get('update_data'):
        await state.update_data(update_data=None)
        await send_message_with_choose_options(message, state)
        return
    
    await state.set_state(Vacancies.show_vacancies)
    await send_vacancies(message, state)

@router.message(Vacancies.experience)
async def choose_experience(message: Message, state: FSMContext):
    exp = message.text

    if exp not in (experience for experience in EXPERIENCE.keys()):
        await message.answer('Выберите опыт работы на клавиатуре!')
        return
    
    id_exp = EXPERIENCE.get(exp)
    await state.update_data(experience=[id_exp, exp])
    await send_message_with_choose_options(message, state)

@router.message(Vacancies.employment)
async def choose_employment(message: Message, state: FSMContext):
    emp = message.text

    if emp not in (employment for employment in EMPLOYMENT.keys()):
        await message.answer('Выберите тип занятости на клавиатуре!')
        return
    
    id_emp = EMPLOYMENT.get(emp)
    await state.update_data(employment=[id_emp, emp])
    await send_message_with_choose_options(message, state)

@router.message(Vacancies.schedule)
async def choose_schedule(message: Message, state: FSMContext):
    sched = message.text

    if sched not in (schedule for schedule in SCHEDULE.keys()):
        await message.answer('Выберите график работы на клавиатуре!')
        return
    
    id_sched = SCHEDULE.get(sched)
    await state.update_data(schedule=[id_sched, sched])
    await send_message_with_choose_options(message, state)

@router.message(Vacancies.show_vacancies)
async def send_more_vacancies(message: Message, state: FSMContext):
    
    if message.text == 'Уточнить параметры поиска':
        await send_message_with_choose_options(message, state)
        
@router.message(Vacancies.additional_options)
async def choose_parameter(message: Message, state: FSMContext):
    num = message.text

    if num == 'Вернуться к поиску':
        await state.set_state(Vacancies.show_vacancies)
        await send_vacancies(message, state)
        return

    if not fullmatch(r'[1-6]', num):
        await message.answer('Выберите цифру чтобы изменить параметр')
        return
    
    match int(num):
        case 1:
            await state.set_state(Vacancies.speciality)
            await state.update_data(update_data=True)
            await message.answer('Выберите специальность по которой нужно найти вакансии или напишите сами',
                          reply_markup=await specialties(message.from_user.id, True))
        case 2:
            await state.set_state(Vacancies.salary)
            await state.update_data(update_data=True)
            data = await state.get_data()
            await message.answer('Выберите желаемую заработную плату\nЕсли она не важна нажмите на \"Пропустить"',
                          reply_markup=await salaries(data['speciality']))
        case 3:
            await state.set_state(Vacancies.area)
            await state.update_data(update_data=True)
            await message.answer('Выберите город в котором нужно найти вакансии или напишите сами',
                         reply_markup=await areas(message.from_user.id, True))
        case 4:
            await state.set_state(Vacancies.experience)
            await message.answer('Выберите опыт работы на клавиатуре',
                         reply_markup=experiences)
        case 5:
            await state.set_state(Vacancies.employment)
            await message.answer('Выберите тип занятости, который вам нужен',
                         reply_markup=employments)
        case 6:
            await state.set_state(Vacancies.schedule)
            await message.answer('Выберите график работы, который удобен для вас',
                         reply_markup=schedules)

async def send_vacancies(message: Message, state: FSMContext):
    data = await state.get_data()
    response = await get_vacancies(**data)
    vacancies = response['items']

    message_vacancies = await to_thread(create_dict_with_vacancies, vacancies, message.from_user.id)
    await message.answer(message_vacancies, parse_mode='html', reply_markup=more_vacancies, disable_web_page_preview=True)

async def send_message_with_choose_options(message: Message, state: FSMContext):
    await state.set_state(Vacancies.additional_options)
    mess = await to_thread(create_message_with_selected_options, await state.get_data())
    await message.answer(mess, parse_mode='html', reply_markup=additional_options)
    await message.answer("""Выберите нужный параметр, отправьте цифру:\n\n1. Специальность\n2. Зарплата
3. Регион\n4. Опыт работы\n5. Тип занятости\n6. График работы\n""")