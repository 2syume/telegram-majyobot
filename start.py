import time

from bot import init_updater
from bot.models import init
from config import Config


def start():
    init(Config.DATABASE_CONNECTION)

    updater = init_updater(Config)
    updater.start_polling()
    # updater.idle()

    print("Bot started!")

    # try:
    #     while True:
    #         time.sleep(1000)
    # except KeyboardInterrupt:
    #     updater.stop()
    #     print("Bot stopped")


if __name__ == "__main__":
    start()

