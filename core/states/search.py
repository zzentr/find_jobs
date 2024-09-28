from asyncio import to_thread

from core.states.imports import *
from core.requestsAPI import get_vacancies
from core.keyboards.reply import more_vacancies
from core.synchronous_functions import create_dict_with_vacancies

router = Router()


class Search(StatesGroup):

    speciality = State()


@router.message(Search.speciality)
async def send_vacancies(message: Message, state: FSMContext):
    speciality = message.text()
    response = await get_vacancies(message.text)
    vacancies = response['items']
    message_vacancies = await to_thread(create_dict_with_vacancies, vacancies, message.from_user.id)
    await message.answer(message_vacancies, parse_mode='html', reply_markup=more_vacancies, disable_web_page_preview=True)
    await state.clear()
