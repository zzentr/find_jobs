from core.states.imports import *
from core.handlers.requestsAPI import search_vacanties
import pprint

router = Router()


class Search(StatesGroup):

    speciality = State()


@router.message(Search.speciality)
async def send_vacancies(message: Message, state: FSMContext):
    response = await search_vacanties(message.text)
    pprint.pprint(response)
    # await message.answer(str(response))
    await message.answer('ладнт')
    await state.clear()