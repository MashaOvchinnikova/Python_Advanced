from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, Field
from wtforms.validators import InputRequired, ValidationError
from typing import Optional

app = Flask(__name__)


class NumberLength:
    """
    Валидатор для ограничения числа по его длине в виде класса

    :arg min: минимальная длина числа в символах
    :arg max: максимальная длина числа в символах
    :arg message: сообщение в случае ошибки валидации, опциональный параметр
    """
    def __init__(self, min=-1, max=-1, message=None):
        self.min = min
        self.max = max
        if not message:
            message = f'Длина поля должна быть не менее {min} и не более {max} символов'
        self.message = message

    def __call__(self, form: FlaskForm, field: Field):
        """
        Принимает на вход форму и поле,
        а в случае ошибки валидации выкидывает ValidationError

        :param form: объект класса FlaskfForm
        :param field: объект класса Field
        :return: Исключение ValidationError в случае ошибки валидации
        """
        field_length = field.data and len(field.data) or 0
        if field_length < self.min or self.max != -1 and field_length > self.max:
            raise ValidationError(self.message)


def number_length(min: int = -1, max: int = -1, message: Optional[str] = None):
    """
    Декоратор для функционального валидатора для ограничения числа по его длине

    :param min: минимальная длина числа в символах
    :param max: максимальная длина числа в символах
    :param message: сообщение в случае ошибки валидации, опциональный параметр
    """
    if not message:
        message = f'Длина поля должна быть не менее {min} и не более {max} символов'

    def _number_length(form: FlaskForm, field: Field):
        """
        Принимает на вход форму и поле,
        а в случае ошибки валидации выкидывает ValidationError

        :param form: объект класса FlaskfForm
        :param field: объект класса Field
        :return: Исключение ValidationError в случае ошибки валидации
        """
        field_length = field.data and len(field.data) or 0
        if field_length < min or max != -1 and field_length > max:
            raise ValidationError(message)

    return _number_length


class RegistrationForm1(FlaskForm):
    """
    Валидация полей формы
    """
    phone1 = StringField(validators=[InputRequired(),
                                     NumberLength(min=10, max=10,
                                                  message='Неверный формат номера телефона')])
    phone2 = StringField(validators=[InputRequired(), number_length(min=10, max=10)])


@app.route('/registration1', methods=['POST'])
def registration():
    form = RegistrationForm1()

    if form.validate_on_submit():
        phone1, phone2 = form.phone1.data, form.phone2.data
        return f'Данные формы:\nномер телефона 1: +7{phone1}\nномер телефона 2: +7{phone2}'

    return f'Неправильный ввод данных, {form.errors}', 400


if __name__ == '__main__':
    app.config['WTF_CSRF_ENABLED'] = False
    app.run(debug=True)
