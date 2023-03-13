import os

output_file_path: str = os.path.relpath(os.path.abspath('output_file.txt'))
binary_labels: list = ['B', 'KiB', 'MiB', 'GiB', 'TiB']


def get_summary_rss(file_path: str) -> str:
    """
    Возвращает суммарный объём потребляемой памяти
    из файла с результатом выполнения команды ps aux в человекочитаемом формате
    :param file_path: Путь до файла с результатом выполнения команды ps aux
    :return: Суммарный объём потребляемой памяти в байтах, килобайтах, мегабайтах, гигабайтах и терабайтах
    """
    summary_rss = 0

    with open(file_path, 'r', encoding='utf-8') as output_file:
        rss_index = next(output_file).split().index('RSS')
        lines = output_file.readlines()[1:]

        for line in lines:
            columns = line.split()
            summary_rss += int(columns[rss_index])

    new_formats = convert_bytes(summary_rss)

    return ', '.join(new_formats)


def convert_bytes(size: int) -> list:
    """
    Переводит байты в килобайты, мегабайты, гигабайты и терабайты
    :param size: Размер файла в байтах
    :return: Размер файла в различных единицах измерения в виде списка
    """
    new_formats = [f'{str(round(size / 1024**power))}{label}' for power, label in enumerate(binary_labels)]
    return new_formats


if __name__ == '__main__':
    print(get_summary_rss(output_file_path))

