from core.states.imports import *
from core.states.search import Vacancies
from core.keyboards import specialties

router = Router()


class Menu(StatesGroup):

    start = State()


@router.message(Menu.start)
async def menu(message: Message, state: FSMContext):
    text = message.text

    if text == 'Искать вакансии':
        await state.set_state(Vacancies.speciality)
        await message.answer('Выберите специальность по которой нужно найти вакансии или напишите сами',
                          reply_markup=await specialties(message.from_user.id))
        
    elif text == 'что-то':
        await message.answer('плохое')

    else: await message.answer('Выберите действие на клавиатуре!')
    