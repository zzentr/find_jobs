from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from asyncio import to_thread

from core.states.imports import *
from core.requestsAPI import search_vacancies
from core.keyboards.reply import more_vacancies

router = Router()
all_vacancies = {}


class Search(StatesGroup):

    speciality = State()


@router.message(Search.speciality)
async def send_vacancies(message: Message, state: FSMContext):
    response = await search_vacancies(message.text)
    message_vacancies = await to_thread(create_message_search, response, message.from_user.id)
    await message.answer(message_vacancies, parse_mode='html', reply_markup=more_vacancies, disable_web_page_preview=True)
    await state.clear()

def create_message_search(response: dict, tg_id: int) -> str:
    vacancies = response['items']
    currencies = {'RUB': 'руб.', 'RUR': 'руб.', 'KZT': 'тенге', 'EUR': 'евро', 'USD': '$'}
    message = '👁 Чтобы посмотреть подробную информацию о вакансии, напишите мне её номер!\n\n'

    for i, vacancy in enumerate(vacancies):
        
        id = vacancy['id']
        name = vacancy['name']
        salary = ''
        area = f'🗺 {vacancy['area']['name']}'
        employer_name = vacancy['employer']['name']
        snippet = ''
        url = f'✔️ Откликнуться: {vacancy['alternate_url']}'

        dash = '\n--------------------------\n\n'
        if i == 4:
            dash = ''

        if vacancy['salary']:

            if vacancy['salary']['from']:
                salary = f'\n{vacancy['salary']['from']} '

            if vacancy['salary']['to']:
                if salary:
                    salary += f'- {vacancy['salary']['to']} '
                else:
                    salary = f'до {vacancy['salary']['to']} '

            salary += currencies[vacancy['salary']['currency']]

        if vacancy['snippet']['responsibility']:
            snippet += (f'Обязанности: {vacancy['snippet']['responsibility'].replace('<highlighttext>', '').replace('</highlighttext>', '')}\n\n')
            
        if vacancy['snippet']['requirement']:
            snippet += (f'Требования: {vacancy['snippet']['requirement'].replace('<highlighttext>', '').replace('</highlighttext>', '')}\n\n')
        
        

        all_vacancies[tg_id] = {i+1: {'id': id, 'name': name, 'salary': salary, 'area': area, 'employer_name': employer_name,
                                    'snippet': snippet, 'url': url}}
        if i >= 5:
            continue
        message += f'<b>{i+1}. {name}</b>\n{salary}\n{area} - {employer_name}\n\n{snippet}{url}{dash}'
        
    return message