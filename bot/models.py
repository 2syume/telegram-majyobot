from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, create_engine
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from traceback import print_exc
from sqlalchemy.ext.declarative import declarative_base
import sys

from . import Global


Base = declarative_base()


def init(db_str):
    engine = create_engine(db_str, echo=True)
    Session = sessionmaker(bind=engine)
    
    Global.db_engine = engine
    Global.db_Session = Session


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    userid = Column(String, unique=True)
    username = Column(String, unique=True)


class Photo(Base):
    __tablename__ = "photo"

    id = Column(Integer, primary_key=True)
    file_id = Column(String)
    file_name = Column(String)
    tag = Column(String)
    comment = Column(String)

    user_id = Column(Integer, ForeignKey(User.id))
    user = relationship("User")

    @classmethod
    def save(cls, file_id, file_name, user_id, user_name, tag, comment):
        try:
            session = Global.db_Session()
            p = Photo()
            p.file_id = file_id
            p.file_name = file_name
            p.tag = tag
            p.comment = comment

            try:
                u = session.query(User).filter(User.username == user_name).one()
            except NoResultFound:
                u = User()
                u.userid = user_id
                u.username = user_name
                session.add(u)
            p.user = u
            session.commit()
            print("Photo info saved to database")
        except:
            session.rollback()
            print_exc()
        

