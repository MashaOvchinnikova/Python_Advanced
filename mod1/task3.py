from flask import Flask
import random

app = Flask(__name__)
cats_list = ['корниш-рекс', 'русская голубая', 'шотландская вислоухая', 'мейн-кун', 'манчкин']


@app.route('/cats')
def cats():
    return random.choice(cats_list)


if __name__ == "__main__":
    app.run(debug=True)
