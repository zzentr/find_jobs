from aiogram import Bot, Dispatcher
from asyncio import run
from dotenv import load_dotenv
import os
load_dotenv()

from core.handlers import commands, reply_text
from core.states import search

bot = Bot(os.getenv('TOKEN'))
dp = Dispatcher()

async def main():
    dp.include_routers(commands.router, reply_text.router, 
    search.router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    run(main())