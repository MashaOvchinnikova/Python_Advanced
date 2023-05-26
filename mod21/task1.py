from datetime import date

from sqlalchemy import Table, Column, Integer, DateTime, Boolean, Float, Date, Text, create_engine, ForeignKey
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy.ext.associationproxy import association_proxy
from typing import Dict, Any


DATABASE_NAME = 'mod21.sqlite'

engine = create_engine(f'sqlite:///{DATABASE_NAME}')

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()


students_books_association = Table(
    'students_books',
    Base.metadata,
    Column('student_id', Integer, ForeignKey('student.id')),
    Column('book_id', Integer, ForeignKey('book.id'))
)


class Book(Base):
    __tablename__ = 'book'
    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    count = Column(Integer, default=1)
    release_date = Column(Date, nullable=False)
    receiving_books = relationship('ReceivingBook', cascade='all, delete-orphan')
    author_id = Column(Integer, ForeignKey('author.id'))
    author = relationship("Author", back_populates="book")
    student = relationship("Student", secondary=students_books_association)

    def to_json(self) -> Dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in
                self.__table__.columns}


class Author(Base):
    __tablename__ = 'author'
    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    surname = Column(Text, nullable=False)
    book = relationship("Book", back_populates="author")


class Student(Base):
    __tablename__ = 'student'
    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    surname = Column(Text, nullable=False)
    phone = Column(Text, nullable=False)
    email = Column(Text, nullable=False)
    average_score = Column(Float, nullable=False)
    scholarship = Column(Boolean, nullable=False)
    receiving_books = relationship('ReceivingBook', cascade='all, delete-orphan')
    borrowed_book = association_proxy('book', 'title')

    @classmethod
    def get_students_in_hostel(cls):
        return session.query(cls).filter(cls.cholarship).all()

    @classmethod
    def get_students_above_avg(cls, avg_score):
        return session.query(cls).filter(cls.average_score > avg_score).all()

    def to_json(self) -> Dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in
                self.__table__.columns}


class ReceivingBook(Base):
    __tablename__ = 'receiving_book'
    student_id = Column(Integer, ForeignKey('student.id'), primary_key=True)
    book_id = Column(Integer, ForeignKey('book.id'), primary_key=True)
    date_of_issue = Column(DateTime, nullable=False)
    date_of_return = Column(DateTime)
    student = relationship('Student')
    book = relationship('Book')

    @hybrid_property
    def count_date_with_book(self):
        if self.return_date is None:
            return (date.today() - self.date_of_issue).days
        else:
            return (self.return_date - self.date_of_issue).days

    def to_json(self) -> Dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in
                self.__table__.columns}


def create_db():
    Base.metadata.create_all(engine)
