import asyncio
from pprint import pprint
import re
from typing import List

import aiohttp
from more_itertools import chunked

from app.models import Session, SwapiPersons, init_db

CHUNK_SIZE = 5


async def get_person_info(person_id, session):
    response = await session.get(f'https://swapi.dev/api/people/{person_id}/')
    data = await response.json()
    return data


async def main_info():
    await init_db()
    session = aiohttp.ClientSession()

    for person_id_chunked in chunked(range(1, 100), CHUNK_SIZE):
        coroutines = [get_person_info(person_id, session) for person_id in person_id_chunked]
        results = await asyncio.gather(*coroutines)
        more_results = await get_close_info(results, session)
        asyncio.create_task(insert_person(more_results))

    await session.close()
    set_of_task = asyncio.all_tasks() - {asyncio.current_task()}
    await asyncio.gather(*set_of_task)


async def get_close_info(results, session):
    res = []
    for Q in results:
        for key, value in Q.items():
            if key == 'films' or key == 'species' or key == 'vehicles' or key == 'starships':
                val = await get_person_more(key, value, session)
                valu = {key: val}
                Q.update(valu)
        res.append(Q)
    return res


async def get_person_more(info_name, info_url, session):
    names = []
    for ids in info_url:
        info_id = re.search(r"/(\d+)/", ids).group(1)
        response = await session.get(f'https://swapi.dev/api/{info_name}/{info_id}/')
        data = await response.json()
        if info_name == 'films':
            names.append(data['title'])
        else:
            names.append(data['name'])
    return ', '.join(names)


async def insert_person(info_dict: List[dict]):
    try:
        async with Session() as session:
            person = [SwapiPersons(
                birth_year=info['birth_year'],
                eye_color=info['eye_color'],
                films=info['films'],
                gender=info['gender'],
                hair_color=info['hair_color'],
                height=info['height'],
                homeworld=info['homeworld'],
                mass=info['mass'],
                name=info['name'],
                skin_color=info['skin_color'],
                species=info['species'],
                starships=info['starships'],
                vehicles=info['vehicles'],
            ) for info in info_dict]
            session.add_all(person)
            await session.commit()
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    asyncio.run(main_info())
