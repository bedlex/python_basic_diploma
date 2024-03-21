""" Entry point for telegram bot """
import time
from app import bot
from app.log import error_log
from app.bot_api.routes import *


if __name__ == "__main__":
    # Going loop true in case if bad internet connection
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as error:
            error_log(error)
            time.sleep(2)