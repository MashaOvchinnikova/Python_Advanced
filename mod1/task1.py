from flask import Flask

app = Flask(__name__)


@app.route('/')
@app.route('/hello_world')
def hello_world():
    return 'Привет, мир!'


if __name__ == '__main__':
    app.run(debug=True)


