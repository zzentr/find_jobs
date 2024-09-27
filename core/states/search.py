from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from asyncio import to_thread

from core.states.imports import *
from core.requestsAPI import search_vacancies
from core.keyboards.reply import more_vacancies

router = Router()
all_vacancies = {}
last_vacancy = {}

class Search(StatesGroup):

    speciality = State()


@router.message(Search.speciality)
async def send_vacancies(message: Message, state: FSMContext):
    response = await search_vacancies(message.text)
    vacancies = response['items']
    message_vacancies = await to_thread(create_dict_with_vacancies, vacancies, message.from_user.id)
    await message.answer(message_vacancies, parse_mode='html', reply_markup=more_vacancies, disable_web_page_preview=True)
    await state.clear()

def create_message_with_vacancies(tg_id: int) -> str:
    global last_vacancy
    if last_vacancy.get(tg_id) is None:
        last_vacancy[tg_id] = 1 
    message = '👁 Чтобы посмотреть подробную информацию о вакансии, напишите мне её номер!\n\n'
    index = 0
    for vacancy_key in all_vacancies[tg_id]:
        if vacancy_key < last_vacancy[tg_id]:
            continue

        if index == 5:
            last_vacancy[tg_id] = vacancy_key
            break
        
        index += 1
        vacancy = all_vacancies[tg_id][vacancy_key]
        
        name = vacancy['name']
        salary = vacancy['salary']
        area = vacancy['area']
        employer_name = vacancy['employer_name']
        snippet = vacancy['snippet']
        url = vacancy['url']

        dash = '\n--------------------------\n\n' if index < 5 else ''

        message += f'<b>{vacancy_key}. {name}</b>\n{salary}\n{area} - {employer_name}\n\n{snippet}{url}{dash}'
        
    return message

def create_dict_with_vacancies(vacancies: dict, tg_id: int) -> str:
    currencies = {'RUB': 'руб.', 'RUR': 'руб.', 'KZT': 'тенге', 'EUR': 'евро', 'USD': '$'}
    all_vacancies[tg_id] = {}

    for i, vacancy in enumerate(vacancies):
        
        id = vacancy['id']
        name = vacancy['name']
        salary = ''
        area = f'🗺 {vacancy['area']['name']}'
        employer_name = vacancy['employer']['name']
        snippet = ''
        url = f'✔️ Откликнуться: {vacancy['alternate_url']}'

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
        
        all_vacancies[tg_id][i+1] = {'id': id, 'name': name, 'salary': salary, 'area': area, 'employer_name': employer_name,
                                    'snippet': snippet, 'url': url}
        
    return create_message_with_vacancies(tg_id)