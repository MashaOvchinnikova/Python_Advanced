from flask import Flask, jsonify, request
import os
from mod20.database import session, Books, ReceivingBooks, create_db, DATABASE_NAME

app = Flask(__name__)


@app.before_request
def before_request_func():
    db_is_created = os.path.exists(DATABASE_NAME)
    if not db_is_created:
        create_db()


@app.route('/books', methods=['GET'])
def get_all_books():
    """Получение списка всех книг в библиотеке"""
    books = session.query(Books).all()
    books_list = []
    for book in books:
        book_as_dict = book.to_json()
        books_list.append(book_as_dict)
    return jsonify(books_list=books_list), 200


@app.route('/debtors', methods=['GET'])
def get_debtors():
    """Получение списка должников, которые держат книги у себя более 14 дней"""
    debtors = session.query(ReceivingBooks).filter(ReceivingBooks().count_date_with_book > 14).all()
    debtors_list = []
    for debtor in debtors:
        debtor_as_dict = debtor.to_json()
        debtors_list.append(debtor_as_dict)
    return jsonify(debtors_list=debtors_list), 200


if __name__ == '__main__':
    app.run()






