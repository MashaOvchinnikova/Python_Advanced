import sys
from typing import Union


def get_mean_size(data: list) -> Union[float, str]:
    """
    Вычисляет средний размер файла в каталоге
    :param data: Список, содержащий информацию о каталогах и файлах, находящихся в папке
    :return: Средний размер файла в каталоге
    """
    if len(data) == 0:
        return 'Файлов в каталоге нет'

    total_files_size = 0

    for line in data:
        file_size = line.rstrip().split()[4]
        if file_size.isdigit():
            total_files_size += int(file_size)
        else:
            return 'Не удается получить размер файла'

    return round(total_files_size / len(data), 2)


if __name__ == '__main__':
    lines = sys.stdin.readlines()[1:]
    print(f'Средний размер файла в каталоге: {get_mean_size(lines)} байт')
