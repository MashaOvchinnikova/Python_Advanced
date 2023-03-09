from flask import Flask
import os
import re
import random

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BOOK_FILE = os.path.join(BASE_DIR, 'war_and_peace.txt')

with open(BOOK_FILE, 'r', encoding='utf-8') as book:
    text = book.read()


@app.route('/get_random_word')
def get_random_word():
    return random.choice(get_words_list())


def get_words_list():
    result = re.findall(r'[а-яa-z\']+', text, flags=re.I)
    return result


if __name__ == "__main__":
    app.run(debug=True)
