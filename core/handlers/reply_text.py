from aiogram import F, Router
from aiogram.types import Message
from asyncio import to_thread
from core.synchronous_functions import create_message_with_vacancies
from core.keyboards import more_vacancies
from main import all_vacancies


router = Router()

@router.message(F.text == 'Показать ещё')
async def show_more_vacancies(message: Message):
    if all_vacancies.get(message.from_user.id):
        message_vacancies = await to_thread(create_message_with_vacancies, message.from_user.id)
        await message.answer(message_vacancies, parse_mode='html', reply_markup=more_vacancies, disable_web_page_preview=True)
    else:
        await message.answer('иди нахуй')
