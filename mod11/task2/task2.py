import logging
import time
import requests
import os
from mod11.task2.gen_database import DATABASE_NAME, create_db, session, StarWarsPerson
import threading

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

URL = "https://swapi.dev/api/people/{}"


def add_person(person: dict):
    person_name, person_gender, person_birth_year = \
        person['name'], \
        person['gender'], \
        person['birth_year']

    new_person = StarWarsPerson(name=person_name,
                                gender=person_gender,
                                birth_year=person_birth_year)
    session.add(new_person)


def get_person(url: str):
    response = requests.get(url)

    if response.status_code != 200:
        return

    add_person(person=response.json())


def load_people_sequential():
    start = time.time()
    for i in range(20):
        get_person(URL.format(i+1))

    session.commit()
    logger.info('Load_people_sequential done in {:.4}'.format(time.time() - start))


def load_people_multithreading():
    start = time.time()
    threads = []
    for i in range(20):
        thread = threading.Thread(target=get_person, args=(URL.format(i+1),))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    session.commit()
    logger.info('Load_people_multithreading done in {:.4}'.format(time.time() - start))


if __name__ == '__main__':
    if not os.path.exists(DATABASE_NAME):
        create_db()
    load_people_sequential()
    load_people_multithreading()
