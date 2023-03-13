from flask import Flask

app = Flask(__name__)
storage = dict()
res = dict()


@app.route('/add/<date>/<int:number>')
def add_expenses(date: str, expense: int):
    """
    Cохраненяет информации о совершённой в рублях трате за какой-то день
    :param date: Дата в формате YYYYMMDD, где YYYY — год, MM — месяц (от 1 до 12), DD — число (от 01 до 31)
    :param expense: сумма потраченных за день денег
    :return:
    """
    year, month, day = int(date[0:4]), int(date[4:6]), int(date[-2:])
    storage.setdefault(year, {}).setdefault(month, {}).setdefault(day, 0)
    res.setdefault(year, {}).setdefault(month, 0)
    storage[year][month][day] += expense
    res[year][month] += expense
    return 'Данные о трате успешно сохранены'


@app.route('/calculate/<int:year>')
def calculate_annual_expenses(year: int):
    """
    Получает суммарные траты за указанный год
    :param year: год
    :return: Инфорация о суммарных тратах за указанный год в виде строки
    """
    monthly_expenses = res[year]
    annual_expenses = sum(monthly_expenses.values())
    return f'Затраты за {year} год: {annual_expenses} рублей'


@app.route('/calculate/<int:year>/<int:month>')
def calculate_annual_and_monthly_expenses(year: int, month: int):
    """
    Получает суммарные траты за указанный год и месяц
    :param year: год
    :param month: месяц
    :return: Инфорация о суммарных тратах за указанный год и месяц в виде строки
    """
    annual_expenses = calculate_annual_expenses(year)
    monthly_expenses = res[year][month]
    return f'{annual_expenses}<br>Затраты за {month}-й месяц: {monthly_expenses} рублей'


if __name__ == '__main__':
    app.run(debug=True)
