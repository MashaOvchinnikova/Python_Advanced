from flask import Flask
from datetime import datetime

app = Flask(__name__)

weekdays_list: list = ['Понедельника', 'Вторника', 'Среды', 'Четверга', 'Пятницы', 'Субботы', 'Воскресенья']


@app.route('/hello_world/<username>')
def hello(username: str) -> str:
    """
    endpoint, который возвращает строку «Привет, <имя> и желает хорошего дня в соответствии с текущим днем недели
    :param username: имя
    :return:
    """
    hello_name = f'Привет, {username}!'
    weekday = datetime.today().weekday()

    if weekday in (0, 1, 3, 6):
        return f'{hello_name} Хорошего {weekdays_list[weekday]}!'

    return f'{hello_name} Хорошей {weekdays_list[weekday]}!'


if __name__ == '__main__':
    app.run(debug=True)
