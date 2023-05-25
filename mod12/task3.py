from threading import Semaphore, Thread, Event
import time
import atexit

sem: Semaphore = Semaphore()


def fun1(event):
    while not event.is_set():
        sem.acquire()
        print(1)
        sem.release()
        time.sleep(0.25)
    print('fun1 done')


def fun2(event):
    while not event.is_set():
        sem.acquire()
        print(2)
        sem.release()
        time.sleep(0.25)
    print('fun2 done')


def stop_background(stop_event, threads):
    stop_event.set()
    for thread in threads:
        thread.join()
    print('Stopping threads done')


def do_something():
    pass


stop_event: Event = Event()
t1: Thread = Thread(target=fun1, daemon=True, args=(stop_event,))
t2: Thread = Thread(target=fun2, daemon=True, args=(stop_event,))

t1.start()
t2.start()

try:
    while True:
        do_something()
except KeyboardInterrupt:
    print('\nReceived keyboard interrupt, quitting threads.')
    atexit.register(stop_background, stop_event, [t1, t2])
    exit(1)
