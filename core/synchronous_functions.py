from main import all_vacancies, all_specialties, all_areas, last_vacancy, CURRENCIES

def create_message_with_vacancies(tg_id: int) -> str:
    global last_vacancy

    if last_vacancy.get(tg_id) is None:
        last_vacancy[tg_id] = 1 

    message = ''
    index = 0
    for vacancy_key in all_vacancies[tg_id]:
        if vacancy_key < last_vacancy[tg_id]:
            continue

        if index == 5:
            if vacancy_key != 50:
                last_vacancy[tg_id] = vacancy_key
            break
        index += 1
        vacancy = all_vacancies[tg_id][vacancy_key]
        
        name = vacancy['name']
        salary = vacancy['salary']
        experience = vacancy['experience']
        employment = vacancy['employment']
        schedule = vacancy['schedule']
        area = vacancy['area']
        employer_name = vacancy['employer_name']
        snippet = vacancy['snippet']
        url = vacancy['url']

        dash = '\n--------------------------\n\n' if index < 5 else ''

        message += f"""<b>{vacancy_key}. {name}</b>\n{salary}\n{area} - {employer_name}\n
{experience}\n{employment}\n{schedule}\n\n{snippet}{url}{dash}"""
        
    return message

def create_dict_with_vacancies(vacancies: dict, tg_id: int) -> str:
    global all_vacancies, last_vacancy
    all_vacancies[tg_id] = {}
    last_vacancy[tg_id] = 1

    for i, vacancy in enumerate(vacancies):
        
        name = vacancy['name']
        salary = ''
        experience = f'<b>Требуемый опыт:</b> {vacancy['experience']['name']}'
        employment = f'<b>Тип занятости:</b> {vacancy['employment']['name']}'
        schedule = f'<b>График работы:</b> {vacancy['schedule']['name']}'
        area = f'🗺 {vacancy['area']['name']}'
        employer_name = vacancy['employer']['name']
        snippet = ''
        url = f'✔️ <b>Откликнуться:</b> {vacancy['alternate_url']}'

        if vacancy['salary']:

            if vacancy['salary']['from']:
                salary = f'💸 {vacancy['salary']['from']} '

            if vacancy['salary']['to']:
                if salary:
                    salary += f'- {vacancy['salary']['to']} '
                else:
                    salary = f'💸 до {vacancy['salary']['to']} '

            salary += CURRENCIES[vacancy['salary']['currency']]

        if vacancy['snippet']['responsibility']:
            snippet += (f'<b>Обязанности:</b> {vacancy['snippet']['responsibility'].replace('<highlighttext>', '').replace('</highlighttext>', '')}\n\n')
            
        if vacancy['snippet']['requirement']:
            snippet += (f'<b>Требования:</b> {vacancy['snippet']['requirement'].replace('<highlighttext>', '').replace('</highlighttext>', '')}\n\n')
        
        all_vacancies[tg_id][i+1] = {'name': name, 'employer_name': employer_name, 'salary': salary, 
                                     'experience': experience, 'employment':employment, 'schedule': schedule, 
                                     'area': area, 'snippet': snippet, 'url': url}
        
    return create_message_with_vacancies(tg_id)

def create_list_all_specialties(response: dict) -> None:
    global all_specialties
    categories = response['categories']

    for category in categories:
        specialties = category['roles']
        for speciality in specialties:
            spec = speciality['name']

            if spec == 'другое':
                return

            spec = spec.split('(')[0]

            if ',' in spec:
                spec = spec.split(', ')
                for spec_clear in spec:
                    all_specialties.append(spec_clear)
                continue

            all_specialties.append(spec)

def create_dict_all_areas(response: list) -> None:
    global all_areas

    for country in response:
        all_areas[country['id']] = country['name'].lower()
        for region in country['areas']:
            all_areas[region['id']] = region['name'].lower()
            for city in region['areas']:
                all_areas[city['id']] = city['name'].lower()           

def check_correct_area(area):

    for key, value in all_areas.items():
        if area == value:
            return int(key) 
    return False