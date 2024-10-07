from core.handlers.states.imports import *
from core.handlers.states.search import Vacancies
from core.keyboards import specialties

router = Router()


class Menu(StatesGroup):

    start = State()


@router.message(Menu.start)
async def menu(message: Message, state: FSMContext):
    text = message.text

    if text == 'Искать вакансии':
        await state.set_state(Vacancies.speciality)
        await state.update_data(speciality=None, salary=None, area=None, experience=None, employment=None, schedule=None)
        await message.answer('Выберите специальность по которой нужно найти вакансии или напишите сами',
                          reply_markup=await specialties(message.from_user.id, True))
        
    elif text == 'что-то':
        await message.answer('плохое')

    else: await message.answer('Выберите действие на клавиатуре!')
    