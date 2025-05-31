import logging

from sqlalchemy import create_engine, Column, String, Integer, CheckConstraint, UniqueConstraint, BigInteger, Date
from sqlalchemy.orm import declarative_base, sessionmaker

# from sqlalchemy.ext.declarative import declarative_base

db_url = 'postgres:1234@localhost:5436/bot_db'
engine = create_engine(f'postgresql+psycopg2://{db_url}')

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    chat_id = Column(BigInteger, nullable=False, unique=True, index=True)
    username = Column(String(50))
    fullname = Column(String(50))
    phone = Column(String(50))
    birthday = Column(Date)
    address = Column(String(200))

    def __repr__(self):
        return f"{self.__class__.__name__}({self.id}, {self.chat_id!r})"

    @classmethod
    def check_register(cls, session, id_):
        obj = session.query(cls).filter(id_ == cls.chat_id).first()
        if not obj:
            return False
        return True

    def save(self, session):
        session.add(self)
        session.commit()
        logging.info(f'{self} obyekt `{self.__tablename__}` jadvalga saqlandi!')

    @classmethod
    def update(cls, session, id_, **kwargs):
        obj = session.query(cls).filter(id_ == cls.id).first()
        if obj:
            for key, value in kwargs.items():
                if hasattr(obj, key):
                    setattr(obj, key, value)
                else:
                    raise KeyError(f'`{key}` attribut `{cls}` jadvalda mavjud emas!')
            session.commit()
            return True
        return False


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
