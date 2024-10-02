from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from core.handlers.states.main_menu import Menu
from core.keyboards import main_menu

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