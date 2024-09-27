import aiohttp

async def search_vacanties(speciality):
    async with aiohttp.ClientSession() as session:
        params = {
            'host': 'hh.ru',
            'text': 'python',
            'per_page': 10,
            'locale': 'RU'
        }
        async with session.get('https://api.hh.ru/vacancies?', params=params) as response:
            return await response.json()