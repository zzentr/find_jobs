from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from asyncio import to_thread

from core.handlers.states.main_menu import Menu
from core.handlers.states.search import Vacancies
from core.keyboards import last_speciality_show, last_city_show, more_vacancies, main_menu, specialties, areas
from core.synchronous_functions import create_message_with_vacancies

router = Router()

@router.message(Command('start'))
async def start(message: Message, state: FSMContext):
    await message.answer('Привет! Я помогу тебе быстро и удобно найти вакансию подходящую именно для тебя '
                         'и изучить рынок: зарплаты, требования к работникам и многое другое!', reply_markup=main_menu)
    await state.set_state(Menu.start)

@router.message(F.text == 'Главное меню')
async def send_main_menu(message: Message, state: FSMContext):
    await message.answer('С чем мне помочь? Выберите действие на клавиатуре для работы со мной!', reply_markup=main_menu)
    await state.set_state(Menu.start)

@router.message(F.text == 'Ещё ⇒')
async def show_more(message: Message, state: FSMContext):
    current_state = await state.get_state()
    tg_id = message.from_user.id
    
    if current_state == Vacancies.speciality.state:
        await message.answer('Выберите специальность по которой нужно найти вакансии или напишите сами',
                          reply_markup=await specialties(message.from_user.id))
        
    elif current_state == Vacancies.area.state:
        await message.answer('Выберите город в котором нужно найти вакансии или напишите сами',
                         reply_markup=await areas(message.from_user.id))
        
    elif current_state == Vacancies.show_vacancies.state:
        message_vacancies = await to_thread(create_message_with_vacancies, message.from_user.id)
        await message.answer(message_vacancies, parse_mode='html', reply_markup=more_vacancies, disable_web_page_preview=True)

    else:
        await message.answer('Выберите действие на клавиатуре!')

@router.message(F.text == '⇐ Назад')
async def show_more(message: Message, state: FSMContext):
    global last_speciality_show, last_city_show
    current_state = await state.get_state()
    tg_id = message.from_user.id

    if current_state == Vacancies.speciality.state and last_speciality_show.get(tg_id) not in (None, 0) :
        last_speciality_show[tg_id] -= 12
        await message.answer('Выберите специальность по которой нужно найти вакансии или напишите сами',
                        reply_markup=await specialties(message.from_user.id))
        
    elif current_state == Vacancies.area.state and last_city_show.get(tg_id) not in (None, 0):
        last_city_show[tg_id] -= 6
        await message.answer('Выберите город в котором нужно найти вакансии или напишите сами',
                         reply_markup=await areas(message.from_user.id))

    else:
        await message.answer('Выберите действие на клавиатуре!')