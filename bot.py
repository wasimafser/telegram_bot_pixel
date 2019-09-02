import logging
import os
import random
import sys

from telegram.ext import Updater, CommandHandler, DictPersistence
from telegram import Bot

# Enabling logging
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger()

# Getting mode, so we could define run function for local and Heroku setup
mode = os.getenv("MODE")
TOKEN = os.getenv("TOKEN")
if mode == "dev":
    def run(updater):
        updater.start_polling()
elif mode == "prod":
    def run(updater):
        PORT = int(os.environ.get("PORT", "8443"))
        HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME")
        # Code from https://github.com/python-telegram-bot/python-telegram-bot/wiki/Webhooks#heroku
        updater.start_webhook(listen="0.0.0.0",
                              port=PORT,
                              url_path=TOKEN)
        updater.bot.set_webhook("https://{}.herokuapp.com/{}".format(HEROKU_APP_NAME, TOKEN))
else:
    logger.error("No MODE specified!")
    sys.exit(1)


def start_handler(update, context):
    # Creating a handler-function for /start command
    user_name = update.effective_user["id"]
    logger.info("User {} started bot".format(user_name))
    update.message.reply_text("Hello {}".format(user_name))


def random_handler(update, context):
    # Creating a handler-function for /random command
    number = random.randint(10, 20)
    logger.info("User {} randomed number {}".format(update.effective_user["id"], number))
    update.message.reply_text("Random number: {}".format(number))


def pin_handler(update, context):
    try:
        replied_message_id = update.effective_message['reply_to_message']['message_id']
        bot.pin_chat_message(chat_id=update.effective_chat['id'], message_id=replied_message_id,
                             disable_notification=True)
    except:
        bot.pin_chat_message(chat_id=update.effective_chat['id'], message_id=update.effective_message['message_id'], disable_notification=True)


def intro_handler(update, context):
    update.message.reply_text("Initialize Yourself :  https://telegra.ph/Introduce-Yourself-09-02")

if __name__ == '__main__':
    logger.info("Starting bot")
    bot = Bot(token=TOKEN)
    bot_perst = DictPersistence()
    updater = Updater(TOKEN, use_context=True, persistence=bot_perst)

    updater.dispatcher.add_handler(CommandHandler("start", start_handler))
    updater.dispatcher.add_handler(CommandHandler("random", random_handler))
    updater.dispatcher.add_handler(CommandHandler("pin", pin_handler))
    updater.dispatcher.add_handler(CommandHandler("intro", intro_handler))

    run(updater)