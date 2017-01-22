import telepot
import time


def create_bot(token, msg_handle=None):
    bot = telepot.Bot(token)
    if not msg_handle:
        from .msg_handle import default_msg_handle
        msg_handle = default_msg_handle
    return bot


class Global(object):
    bot = None
    archiever = None

    db_engine = None
    db_Session = None