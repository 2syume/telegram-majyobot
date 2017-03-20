import time
import logging
from telegram.ext import Updater, MessageHandler, Filters

from .config import config
from .models import save_photo_record, save_text_message
from .handlers import save_photo

logger = logging.getLogger(__name__)


def echo(bot, update):
    print("[{}] {}: {}".format(
        update.message.chat.title,
        update.message.from_user.name,
        update.message.text)
    )
    save_text_message(update.message)


def start():
    bot_token = config.get("Bot", "Token")
    updater = Updater(token=bot_token)

    echo_handler = MessageHandler(Filters.text, echo)
    updater.dispatcher.add_handler(echo_handler)

    photo_handler = MessageHandler(Filters.photo, save_photo.handler)
    updater.dispatcher.add_handler(photo_handler)

    updater.start_polling()
