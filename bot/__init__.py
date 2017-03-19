import time
from telegram.ext import Updater, MessageHandler, Filters

def echo(bot, update):
    print("{}: {}".format(
        update.message.from_user.name,
        update.message.text)
        )

def echo_photo(bot, update):
    print("{} sent a photo".format(update.message.from_user.name))


def init_updater(config):
    updater = Updater(token=config.BOT_TOKEN)

    echo_handler = MessageHandler(Filters.text, echo)
    updater.dispatcher.add_handler(echo_handler)

    photo_handler = MessageHandler(Filters.photo, echo_photo)
    updater.dispatcher.add_handler(photo_handler)

    return updater
