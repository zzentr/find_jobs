from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from core.states.search import Search

router = Router()

@router.message(Command('start'))
async def start(message: Message):
    await message.answer('Привет! Я помогу тебе быстро и удобно найти вакансию подходящую именно для тебя '
                         'и изучить рынок: зарплаты, требования к работникам и многое другое!')
    
@router.message(Command('search'))
async def search_vacancies(message: Message, state: FSMContext):
    await state.set_state(Search.speciality)
    await message.answer('Напишите специальность по которой нужно найти вакансии. Без цифр и символов, только буквы')