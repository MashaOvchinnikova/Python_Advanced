from flask import Flask

app = Flask(__name__)


@app.route('/max_number/<path:numbers>')
def max_number(numbers: str) -> str:
    """
    endpoint, который возвращает выделенное курсивом наибольшее из переданных чисел
    :param numbers: список чисел, разделённых слешем /
    :return:
    """
    numbers_list = numbers.split('/')
    is_digits_list = [x.isdigit() for x in numbers_list]

    if all(is_digits_list):
        mx_number = max(map(int, numbers_list))
        return f'Максимальное число: <i>{mx_number}</i>'

    return f'Вместо чисел было передано что-то другое'


if __name__ == '__main__':
    app.run(debug=True)

