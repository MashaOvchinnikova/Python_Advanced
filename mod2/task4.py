from flask import Flask
from datetime import datetime

app = Flask(__name__)

weekdays_dict: dict = {0: 'Понедельника',
                       1: 'Вторника',
                       2: 'Среды',
                       3: 'Четверга',
                       4: 'Пятницы',
                       5: 'Субботы',
                       6: 'Воскресенья'}


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
        return f'{hello_name} Хорошего {weekdays_dict[weekday]}!'

    return f'{hello_name} Хорошей {weekdays_dict[weekday]}!'


if __name__ == '__main__':
    app.run(debug=True)
