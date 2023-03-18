import shlex
import subprocess

from flask import Flask, request

app = Flask(__name__)


@app.route('/ps', methods=['GET'])
def _ps():
    """
    GET-endpoint, который принимает на вход аргументы командной строки,
    а возвращает результат работы команды ps с этими аргументами

    :return: Результат работы команды ps с переданными аргументами
    """
    args: str = ''.join(request.args.getlist('arg'))
    command_str = 'ps ' + shlex.quote(args)
    command = shlex.split(command_str)
    result = subprocess.run(command, capture_output=True, encoding='utf-8')
    if result.returncode == 0:
        data = result.stdout
        return f'<pre>{data}</pre>'
    else:
        return 'Что-то пошло не так', 500


if __name__ == '__main__':
    app.run(debug=True)
