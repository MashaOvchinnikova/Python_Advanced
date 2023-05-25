from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import declarative_base, sessionmaker
from typing import Dict, Any

DATABASE_NAME = 'StarWarsMod12.sqlite'

engine = create_engine(f'sqlite:///{DATABASE_NAME}')
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()


class StarWarsCharacters(Base):
    __tablename__ = 'characters'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    gender = Column(String, nullable=False)
    birth_year = Column(String, nullable=False)

    def to_json(self) -> Dict[str, Any]:
        return {c.name: str(getattr(self, c.name)) for c in
                self.__table__.columns}


def create_db():
    Base.metadata.create_all(engine)
