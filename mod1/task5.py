from flask import Flask
from datetime import datetime, timedelta

app = Flask(__name__)


@app.route('/get_time/future')
def get_future_time():
    delta = timedelta(hours=1)
    current_time_after_hour = datetime.now() + delta
    return f'Точное время через час будет: {current_time_after_hour.strftime("%H:%M:%S")}'


if __name__ == "__main__":
    app.run(debug=True)
