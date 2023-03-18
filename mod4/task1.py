from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import InputRequired, Email, NumberRange

app = Flask(__name__)


class RegistrationForm(FlaskForm):
    """Валидация полей формы

    Attributes:
        email: текст, обязательно для заполнения, валидация формата
        phone: число, обязательно для заполнения, длина — десять символов, только положительные числа
        name: текст, обязательно для заполнения
        address: текст, обязательно для заполнения
        index: число, обязательно для заполнения
        comment: текст, необязательно для заполнения
    """
    email = StringField(validators=[InputRequired(message='"Это поле обязательно для заполнения'),
                                    Email(message='Email указан неверно')])
    phone = IntegerField(validators=[InputRequired(message='"Это поле обязательно для заполнения'),
                                     NumberRange(min=1000000000, max=9999999999)])
    name = StringField(validators=[InputRequired(message='"Это поле обязательно для заполнения')])
    address = StringField(validators=[InputRequired(message='"Это поле обязательно для заполнения')])
    index = IntegerField(validators=[InputRequired(message='"Это поле обязательно для заполнения')])
    comment = StringField()


@app.route('/registration', methods=['POST'])
def registration():
    form = RegistrationForm()

    if form.validate_on_submit():
        email, phone, name, address, index, comment = form.email.data, form.phone.data, form.name.data, \
            form.address.data, form.index.data, form.comment.data

        return f'Пользователь {name} упешно зарегистрирован.\n' \
               f'Данные пользователя:\nemail: {email},\nтелефон: {phone},' \
               f'\nадрес: {address},\nпочтовый индекс: {index},\nкоментарии по доставке: {comment}'

    return f'Неправильный ввод данных, {form.errors}', 400


if __name__ == '__main__':
    app.config['WTF_CSRF_ENABLED'] = False
    app.run(debug=True)
