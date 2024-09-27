from aiogram import F, Router
from aiogram.types import Message
from asyncio import to_thread
from core.states import search as se
from core.keyboards.reply import more_vacancies


router = Router()

@router.message(F.text == 'Показать ещё')
async def show_more_vacancies(message: Message):
    message_vacancies = await to_thread(se.create_message_with_vacancies, message.from_user.id)
    await message.answer(message_vacancies, parse_mode='html', reply_markup=more_vacancies, disable_web_page_preview=True)
