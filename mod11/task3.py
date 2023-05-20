import logging
import random
import threading
import time

TOTAL_TICKETS = 10
SEATS_NUMBER = 12


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Director(threading.Thread):
    def __init__(self, semaphore: threading.Semaphore, sellers_count: int):
        super().__init__()
        self.sem = semaphore
        self.sellers = sellers_count
        logger.info('Director started work')

    def run(self):
        global TOTAL_TICKETS
        is_running = True
        while is_running:
            if TOTAL_TICKETS >= SEATS_NUMBER:
                break
            if TOTAL_TICKETS in (self.sellers, self.sellers+1):
                with self.sem:
                    new_tickets = random.randint(1, 10)
                    TOTAL_TICKETS += new_tickets
                    logger.info(f'Director added {new_tickets} tickets;  '
                                f'{TOTAL_TICKETS} now')
        logger.info(f'Director ran out out of tickets')

    def random_sleep(self):
        time.sleep(random.randint(0, 1))


class Seller(threading.Thread):

    def __init__(self, semaphore: threading.Semaphore):
        super().__init__()
        self.sem = semaphore
        self.tickets_sold = 0
        logger.info('Seller started work')

    def run(self):
        global TOTAL_TICKETS
        is_running = True
        while is_running:
            self.random_sleep()
            with self.sem:
                if TOTAL_TICKETS <= 0:
                    break
                self.tickets_sold += 1
                TOTAL_TICKETS -= 1
                logger.info(f'{self.getName()} sold one;  {TOTAL_TICKETS} left')

        logger.info(f'Seller {self.getName()} sold {self.tickets_sold} tickets')

    def random_sleep(self):
        time.sleep(random.randint(0, 1))


def main():
    semaphore = threading.Semaphore()
    sellers_number = 3
    workers = []

    director = Director(semaphore, sellers_number)
    director.start()
    workers.append(director)

    for _ in range(sellers_number):
        seller = Seller(semaphore)
        seller.start()
        workers.append(seller)

    for worker in workers:
        worker.join()


if __name__ == '__main__':
    main()
