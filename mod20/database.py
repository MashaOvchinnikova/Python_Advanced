from sqlalchemy import create_engine, Column, String, Integer, Date, DateTime, Boolean, Float
from sqlalchemy.orm import declarative_base, sessionmaker
from typing import Dict, Any
from datetime import datetime
from sqlalchemy.ext.hybrid import hybrid_property

DATABASE_NAME = 'mod20.sqlite'

engine = create_engine(f'sqlite:///{DATABASE_NAME}')
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()


# таблица книг в библиотеке
class Books(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    count = Column(Integer, default=1)
    release_date = Column(Date, nullable=False)
    author_id = Column(Integer, nullable=False)

    def __repr__(self):
        return f'Название книги: {self.name},\nКоличество: {self.count},\n' \
               f'Дата выпуска: {self.release_date},\nID автора: {self.author_id}'

    def to_json(self) -> Dict[str, Any]:
        return {c.name: str(getattr(self, c.name)) for c in
                self.__table__.columns}


# таблица авторов
class Authors(Base):
    __tablename__ = 'authors'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)

    def __repr__(self):
        return f'Имя автора: {self.name},\nФамилия: {self.surname}'

    def to_json(self) -> Dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in
                self.__table__.columns}


# таблица читателей
class Students(Base):
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    email = Column(String, nullable=False)
    average_score = Column(Float, nullable=False)
    scholarship = Column(Boolean, default=False)

    def __repr__(self):
        return f'Имя студента: {self.name},\nФамилия: {self.surname},\n' \
               f'Телефон: {self.phone},\nEmail: {self.email},\nСредний бал: {self.average_score}'

    def to_json(self) -> Dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in
                self.__table__.columns}

    @classmethod
    def get_students_who_lives_in_dorm(cls):
        # получить список студентов, которые живут в общежитии
        return session.query(Students).filter(Students.scholarship is True).all()

    @classmethod
    def get_students_with_better_average_score(cls, score: float):
        # получить список студентов, у которых средний балл выше,
        # чем тот балл, который будет передан входным параметром в функцию
        return session.query(Students).filter(Students.average_score > score).all()


# таблица выдачи книг студентам
class ReceivingBooks(Base):
    __tablename__ = 'receiving_books'

    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, nullable=False)
    student_id = Column(Integer, nullable=False)
    date_of_issue = Column(DateTime, nullable=False)
    date_of_return = Column(DateTime)

    def __repr__(self):
        return f'ID книги: {self.book_id},\nID студента, которому выдана книга: {self.student_id},\n' \
               f'Дата выдачи: {self.date_of_issue},\n' \
               f'Дата возврата: {self.date_of_return if self.date_of_return else "Не возвращена"}'

    def to_json(self) -> Dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in
                self.__table__.columns}

    @hybrid_property
    def count_date_with_book(self):
        if self.date_of_return is not None and self.date_of_issue is not None:
            period = self.date_of_return.date() - self.date_of_issue.date()
            days = period.days
            return days
        elif self.date_of_issue is not None:
            now = datetime.now().date()
            period = now - self.date_of_issue.date()
            days = period.days
            return days
        else:
            return 0


def create_db():
    Base.metadata.create_all(engine)












