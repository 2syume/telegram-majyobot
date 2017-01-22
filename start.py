from bot import create_bot, Global
from bot.msg_handle import my_msg_handle
from bot.msg_arc import MessageArchiver
from bot.models import init
from config import Config
import time


def start():
    bot = create_bot(Config.BOT_TOKEN, my_msg_handle)

    Global.config = Config
    Global.archiever = MessageArchiver(bot, Config)

    init(Config.DATABASE_CONNECTION)

    bot.message_loop(my_msg_handle)
    print("Bot started!")

    try:
        while True:
            time.sleep(1000)
    except KeyboardInterrupt:
        print("Bot stopped")


if __name__ == "__main__":
    start()

