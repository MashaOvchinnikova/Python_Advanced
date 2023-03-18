from flask import Flask
import subprocess

app = Flask(__name__)


@app.route('/uptime', methods=['GET'])
def _uptime():
    """
    Endpoint, который в ответ на запрос выводит показатель того, как долго текущая система не перезагружалась

    :return: Строка вида "Current uptime is {UPTIME}",
        где UPTIME — uptime системы (показатель того, как долго текущая система не перезагружалась).
    """
    commands = ['uptime', '-p']
    result = subprocess.run(commands, capture_output=True, encoding='utf-8')
    if result.returncode == 0:
        data = result.stdout
        uptime = data.split('up')[1]
        return f"Current uptime is {uptime}"
    else:
        return 'Что-то пошло не так', 500


if __name__ == '__main__':
    app.run(debug=True)
