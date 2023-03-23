import os
import shlex
import signal
import subprocess


def start_server(port: int):
    """
    Функция, которая на вход принимает порт и запускает по нему сервер.
    Если порт будет занят, она должна найти процесс по этому порту,
    завершить его и попытаться запустить сервер ещё раз.
    :param port: номер порта
    """

    command_str = 'lsof -i :{0}'.format(str(port))
    command: list[str] = shlex.split(command_str)

    process = subprocess.run(command, capture_output=True, text=True)
    port_processes: list[str] = process.stdout.split('\n')[1:]
    for proc in port_processes:
        data = [x for x in proc.split() if x != '']
        if len(proc) <= 1:
            continue
        os.kill(int(data[1]), signal.SIGKILL)

    try:
        subprocess.run(['python', 'test_file.py'], check=True)
    except subprocess.CalledProcessError as e:
        print(e)


if __name__ == "__main__":
    start_server(port=5000)
