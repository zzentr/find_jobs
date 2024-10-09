import aiohttp

async def get_vacancies(speciality: str, area: int | None, salary: int | None,
                         experience: str = None, employment: str = None, schedule: str = None, update_data = None) -> dict:
    async with aiohttp.ClientSession() as session:
        params = {
            'host': 'hh.ru',
            'text': speciality,
            'per_page': 50,
            'locale': 'RU'
        }
        if area: params['area'] = area[0]
        if salary: params['salary'] = salary
        if experience: params['experience'] = experience[0]
        if employment: params['employment'] = employment[0]
        if schedule: params['schedule'] = schedule[0]

        try:
            async with session.get('https://api.hh.ru/vacancies?', params=params) as response:
                if response.ok:
                    return await response.json()
                else:
                    return '404'
        except Exception as er:
            print(f'Error: {er}')
            return False
        
async def get_salary_for_speciality(speciality: str) -> dict:
    async with aiohttp.ClientSession() as session:
        params = {
            'host': 'hh.ru',
            'text': speciality,
            'clusters': 'true',
            'per_page': 0,
            'locale': 'RU'
        }
        async with session.get('https://api.hh.ru/vacancies?', params=params) as response:
            return await response.json()

async def get_all_specialties() -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get('https://api.hh.ru/professional_roles') as response:
            return await response.json()
        
async def get_all_areas() -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get('https://api.hh.ru/areas') as response:
            return await response.json()