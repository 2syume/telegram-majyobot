import logging
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, create_engine
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from traceback import print_exc
from sqlalchemy.ext.declarative import declarative_base, DeferredReflection
import sys
from contextlib import contextmanager

from .config import config


logger = logging.getLogger(__name__)

Base = declarative_base()
db_connstr = config.get('Database', 'DatabaseUrl')
engine = create_engine(db_connstr, echo=True) 
Session = sessionmaker(bind=engine)

def prepare():
    Base.prepare(engine)

@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = Session()
    try:
        yield session
        session.commit()
    except:
        logger.exception(sys.exc_info())
        session.rollback()
        raise
    finally:
        session.close()

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=False)
    # telegram_user_id = Column(String, unique=True)
    username = Column(String)
    firstname = Column(String)
    lastname = Column(String)

    def __init__(self, **kwargs):
        telegram_user = kwargs.get("telegram_user", None)
        if telegram_user:
            self.id = telegram_user.id
            self.username = telegram_user.username
            self.firstname = telegram_user.first_name
            self.lastname = telegram_user.last_name
        else:
            self.id = kwargs.get("id", None)
            self.username = kwargs.get("username", None)
            self.firstname = kwargs.get("firstname", None)
            self.lastname = kwargs.get("lastname", None)


class Chat(Base):
    __tablename__ = "chat"

    id = Column(Integer, primary_key=True, autoincrement=False)
    # telegram_chat_id = Column(Integer, unique=True)
    type_str = Column(String)
    title = Column(String)
    username = Column(String)
    firstname = Column(String)
    lastname = Column(String)

    def __init__(self, **kwargs):
        telegram_chat = kwargs.get("telegram_chat", None)
        if telegram_chat:
            self.id = telegram_chat.id
            self.type_str = telegram_chat.type
            self.title = telegram_chat.title
            self.username = telegram_chat.username
            self.firstname = telegram_chat.first_name
            self.lastname = telegram_chat.last_name
        else:
            self.id = kwargs.get("id", None)
            self.type_str = kwargs.get("type_str", None)
            self.title = kwargs.get("title", None)
            self.username = kwargs.get("username", None)
            self.firstname = kwargs.get("firstname", None)
            self.lastname = kwargs.get("lastname", None)


class Message(Base):
    __tablename__ = "message"

    id = Column(Integer, primary_key=True)
    telegram_message_id = Column(Integer)
    chat_id = Column(Integer, ForeignKey(Chat.id))
    from_user_id = Column(Integer, ForeignKey(User.id))
    date = Column(DateTime)
    text = Column(String)

    chat = relationship(Chat)
    from_user = relationship(User)

    def __init__(self, **kwargs):
        telegram_message = kwargs.get("telegram_message", None)
        if telegram_message:
            self.telegram_message_id = telegram_message.message_id
            self.chat_id = telegram_message.chat.id
            self.from_user_id = telegram_message.from_user.id
            self.date = telegram_message.date
            self.text = telegram_message.text
        else:
            self.id = kwargs.get("id", None)
            self.chat_id = kwargs.get("chat_id", None)
            self.from_user_id = kwargs.get("from_user_id", None)
            self.date = kwargs.get("date", None)
            self.text = kwargs.get("text", None)


class Photo(Base):
    __tablename__ = "photo"

    id = Column(Integer, primary_key=True)
    message_id = Column(Integer, ForeignKey(Message.id))
    file_id = Column(String)
    width = Column(Integer)
    height = Column(Integer)
    file_size = Column(Integer)

    filename = Column(String)
    uuid = Column(String, unique=True)
    url = Column(String)

    message = relationship(Message)

    def __init__(self, **kwargs):
        telegram_photosize = kwargs.get("telegram_photosize", None)
        self.message_id = kwargs.get("message_id", None)
        self.message = kwargs.get("message_obj", None)
        self.filename = kwargs.get("filename", None)
        self.uuid = kwargs.get("uuid", None)
        self.url = kwargs.get("url", None)

        if telegram_photosize:
            self.file_id = telegram_photosize.file_id
            self.width = telegram_photosize.width
            self.height = telegram_photosize.height
            self.file_size = telegram_photosize.file_size
        else:
            self.file_id = kwargs.get("file_id", None)
            self.width = kwargs.get("width", None)
            self.height = kwargs.get("height", None)
            self.file_size = kwargs.get("file_size", None)


def save_text_message(message):
    with session_scope() as dbsession:
        from_user = dbsession.query(User).\
            filter(User.id==message.from_user.id).\
            one_or_none()
        if not from_user:
            from_user = User(telegram_user=message.from_user)
            dbsession.add(from_user)
        
        chat = dbsession.query(Chat).\
            filter(Chat.id == message.chat.id).\
            one_or_none()
        if not chat:
            chat = Chat(telegram_chat=message.chat)
            dbsession.add(chat)

        msg = Message(telegram_message=message)
        dbsession.add(msg)


def save_photo_record(message, photosize, photo_filename, photo_uuid, photo_url):
    with session_scope() as dbsession:
        from_user = dbsession.query(User).\
            filter(User.id==message.from_user.id).\
            one_or_none()
        if not from_user:
            from_user = User(telegram_user=message.from_user)
            dbsession.add(from_user)
        
        chat = dbsession.query(Chat).\
            filter(Chat.id == message.chat.id).\
            one_or_none()
        if not chat:
            chat = Chat(telegram_chat=message.chat)
            dbsession.add(chat)

        msg = dbsession.query(Message).\
            filter(Message.telegram_message_id == message.message_id, Message.chat_id == message.chat.id).\
            one_or_none()
        if not msg:
            msg = Message(telegram_message=message)
            dbsession.add(msg)

        photo = Photo(telegram_photosize=photosize,
                      message_obj=msg,
                      filename=photo_filename,
                      uuid=photo_uuid,
                      url=photo_url)
        dbsession.add(photo)


    