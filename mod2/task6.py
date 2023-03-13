from flask import Flask
import os

app = Flask(__name__)


@app.route('/preview/<int:size>/<path:relative_path>')
def get_preview(size: int, relative_path: str) -> str:
    """
    endpoint, который показывает превью файла, возвращая первые SIZE символов файла по указанному в RELATIVE_PATH пути
    :param size: количество символов, которое нужно прочитать в файле
    :param relative_path: относительный путь до файла
    :return: Две строки. В первой строке содержится информация о файле:
     его абсолютный путь и размер файла в символах, а во второй строке — первые SIZE символов из файла:
    """
    abs_path = os.path.abspath(relative_path)

    if not os.path.exists(abs_path):
        return 'Не удалось найти файл по такому пути'

    with open(abs_path, 'r', encoding='utf-8') as file:
        result_text = file.read(size)
        result_size = 0
        for line in result_text:
            result_size += len(line.rstrip('\n\r'))
    return f'<b>{abs_path}</b> {result_size}<br>{result_text}'


if __name__ == '__main__':
    app.run(debug=True)




