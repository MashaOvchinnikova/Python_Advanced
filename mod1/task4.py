from flask import Flask
from datetime import datetime

app = Flask(__name__)


@app.route('/get_time/now')
def get_current_time():
    current_time = datetime.now().strftime("%H:%M:%S")
    return f'Текущее время: {current_time}'


if __name__ == "__main__":
    app.run(debug=True)
