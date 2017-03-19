from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, create_engine
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from traceback import print_exc
from sqlalchemy.ext.declarative import declarative_base, DeferredReflection
import sys


Base = declarative_base(cls=DeferredReflection)


def init(db_str):
    engine = create_engine(db_str, echo=True) 
    Session = sessionmaker(bind=engine)
    Base.prepare(engine)
    return engine, Session


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    userid = Column(String, unique=True)
    username = Column(String)
    firstname = Column(String)
    lastname = Column(String)


class Message(Base):
    __tablename__ = "message"

    id = Column(Integer, primary_key=True)
    telegram_message_id = Column(Integer)
    from_user_id = Column(Integer, ForeignKey(User.id))
    date = Column(DateTime)

    from_user = relationship(User)


class Photo(Base):
    __tablename__ = "photo"

    id = Column(Integer, primary_key=True)
    message_id = Column(Integer, ForeignKey(Message.id))
    file_id = Column(String)
    width = Column(Integer)
    height = Column(Integer)
    file_size = Column(Integer)

    local_path = Column(String)
