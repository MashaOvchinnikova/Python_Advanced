import logging
import time
import requests
import os
from mod12.task1.gen_database import DATABASE_NAME, create_db, session, StarWarsCharacters
from multiprocessing import cpu_count, Pool
from multiprocessing.pool import ThreadPool

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

URL = "https://swapi.dev/api/people/{}"
INPUT_VALUE = [URL.format(i) for i in range(1, 21)]


def add_character(character: dict):
    character_name, character_gender, character_birth_year = \
        character['name'], \
        character['gender'], \
        character['birth_year']

    new_character = StarWarsCharacters(name=character_name,
                                       gender=character_gender,
                                       birth_year=character_birth_year)
    session.add(new_character)


def get_character_with_threadpool(url: str):
    response = requests.get(url, timeout=(5, 5))

    if response.status_code != 200:
        return

    add_character(character=response.json())


def get_character_with_processpool(url: str):
    response = requests.get(url, timeout=(5, 5))
    if response.status_code != 200:
        return

    add_character(character=response.json())
    session.commit()


def load_characters_with_threadpool():
    pool = ThreadPool(processes=cpu_count() + 5)
    start = time.time()
    result = pool.map(get_character_with_threadpool, INPUT_VALUE)
    pool.close()
    pool.join()
    session.commit()
    end = time.time()
    logger.info('Loading time with threads pool: {} seconds'.format(end - start))


def load_characters_with_processpool():
    start = time.time()
    with Pool(processes=cpu_count()) as pool:
        result = pool.map(get_character_with_processpool, INPUT_VALUE)

    end = time.time()
    logger.info('Loading time with processes pool: {} seconds'.format(end - start))


if __name__ == '__main__':

    if not os.path.exists(DATABASE_NAME):
        create_db()
    load_characters_with_threadpool()
    load_characters_with_processpool()

