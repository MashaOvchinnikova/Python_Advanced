import os
from mod21.task1 import Book, Author, Student, ReceivingBook, session, create_db, DATABASE_NAME
import datetime
from flask import Flask, jsonify
from sqlalchemy import func, extract, desc
from datetime import date


app = Flask(__name__)


@app.before_request
def before_request_func():
    db_is_created = os.path.exists(DATABASE_NAME)
    if not db_is_created:
        create_db()


# Количество оставшихся в библиотеке книг по автору
@app.route('/books/remaining/<int:author_id>', methods=['GET'])
def get_remaining_books(author_id):
    author = session.query(Author).filter(Author.id == author_id).first()

    if author is None:
        return f"Автор с id={author_id} не найден", 400

    count = 0
    for book in author.book:
        count += book.count

    return jsonify({f'Количество оставшихся книг у автора с id={author_id}': count})


# Список книг, которые студент не читал, при этом другие книги этого автора студент уже брал
@app.route('/books/unread/<int:student_id>', methods=['GET'])
def get_unread_books(student_id):
    student = session.query(Student).get(student_id)
    if not student:
        return f"Студент с id={student_id} отсутстует", 400

    student_book_ids = [receiving_book.book_id for receiving_book in student.receiving_books]

    author_book_ids = session.query(Book.id).filter(
        Book.author_id.in_([book.author_id for book in student.receiving_books])).subquery()

    unread_books = session.query(Book).filter(Book.id.in_(author_book_ids)).filter(~Book.id.in_(student_book_ids)).all()

    return jsonify({'Список прочтенных книг': [book.name for book in unread_books]})


# Среднее количество книг, которые студенты брали в этом месяце
@app.route('/books/average', methods=['GET'])
def get_average_books():
    current_month = datetime.datetime.now().month

    books_count = session.query(func.avg(func.count(ReceivingBook.book_id))) \
        .filter(extract('date_of_issue', ReceivingBook.received_date) == current_month).scalar()

    return f"Среднее количество книг, которые были взяты студенами за текущий месяц равно {books_count}"


# Самая популярная книга среди студентов, у которых средний балл больше 4.0
@app.route('/books/popular', methods=['GET'])
def get_popular_book():
    popular_book = session.query(ReceivingBook.book_id, func.count(ReceivingBook.book_id)). \
        join(Student). \
        filter(Student.average_score > 4.0). \
        group_by(ReceivingBook.book_id). \
        order_by(func.count(ReceivingBook.book_id).desc()). \
        first()

    if popular_book:
        book = session.query(Book).get(popular_book[0])
        return f"Самая популярная книга студентов, у которых средний рейтинг выше 4.0 {book.name}"
    else:
        return "Самая популярная книга отсутствует."


# ТОП-10 самых читающих студентов в этом году
@app.route('/students/top-10-readers', methods=['GET'])
def get_top_readers():
    current_year = date.today().year
    top_readers = session.query(Student). \
        join(ReceivingBook). \
        filter(func.extract('year', ReceivingBook.received_date) == current_year). \
        group_by(Student). \
        order_by(desc(func.count(ReceivingBook.id))). \
        limit(10). \
        all()

    top_readers_data = []
    for reader in top_readers:
        reader_data = {
            'id': reader.id,
            'name': reader.name,
            'books_borrowed': len(reader.receiving_books)
        }
        top_readers_data.append(reader_data)

    return jsonify({'top_readers': top_readers_data})


if __name__ == '__main__':
    app.run()
