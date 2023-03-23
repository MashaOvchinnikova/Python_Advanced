import shlex
import subprocess

from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import InputRequired, NumberRange

app = Flask(__name__)


class RunCodeForm(FlaskForm):
    """Валидация полей формы

    Attributes:
        code: строка, обязательно для заполнения
        time_out: положительное число не больше 30, обязательно для заполнения
    """
    code = StringField(
        validators=[
            InputRequired(message='Это поле обязательно для заполнения')
        ])

    time_out = IntegerField(
        validators=[
            InputRequired(message='Это поле обязательно для заполнения'),
            NumberRange(min=0, max=30, message='Тайм-аут не должен превышать 30 секунд')
        ])


@app.route('/run_code', methods=['POST'])
def run_code():
    """
    Endpoint, который принимает на вход код на Python и тайм-аут в секундах.
    Пользователю возвращается результат работы программы,
    а если время, отведённое на выполнение кода, истекло,
    то процесс завершается, после чего отправляется сообщение о том,
    что исполнение кода не уложилось в данное время.
    """
    form = RunCodeForm()

    if form.validate_on_submit():
        code, time_out = form.code.data, form.time_out.data
        command_str = 'prlimit --nproc=1:1 python -c {code}'.format(code=shlex.quote(code))
        command: list[str] = shlex.split(command_str)

        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        try:
            outs, errors = process.communicate(timeout=time_out)
        except subprocess.TimeoutExpired:
            process.kill()
            return f'Исполнение кода не уложилось в данное время: {time_out} секунд', 400
        else:
            if process.returncode == 0:
                return f'Результат работы программы {code}: {outs}'
            return f'При работе программы возникла ошибка: {errors}'

    return f'Неправильный ввод данных, {form.errors} ', 400


if __name__ == '__main__':
    app.config['WTF_CSRF_ENABLED'] = False
    app.run(debug=True)
