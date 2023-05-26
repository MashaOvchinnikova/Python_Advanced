import csv
from flask import Flask, request
from mod21.task1 import Student, session

app = Flask(__name__)

UPLOAD_FOLDER = 'static/files'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/students/upload', methods=['POST'])
def upload_students():
    file = request.files['file']
    students = []
    for row in csv.DictReader(file, delimiter=';'):
        student_data = {
            'name': row['name'],
            'surname': row['surname'],
            'phone': row['phone'],
            'email': row['email'],
            'average_score': float(row['average_score']),
            'scholarship': row['scholarship']
        }
        students.append(student_data)

    try:
        session.bulk_insert_mappings(Student, students)
        session.commit()
        return 'Студенты успешно загружены'
    except:
        return "Произошла какая-то ошибка", 500


if __name__ == '__main__':
    app.run()
