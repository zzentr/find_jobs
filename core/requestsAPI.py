import aiohttp

async def get_vacancies(speciality: str) -> dict:
    async with aiohttp.ClientSession() as session:
        params = {
            'host': 'hh.ru',
            'text': speciality,
            'per_page': 50,
            'locale': 'RU'
        }
        async with session.get('https://api.hh.ru/vacancies?', params=params) as response:
            return await response.json()
        
async def get_all_specialties() -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get('https://api.hh.ru/professional_roles') as response:
            return await response.json()