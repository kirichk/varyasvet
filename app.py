import os
import checker
from pathlib import Path
from dotenv import load_dotenv
from telegram import Bot
from telegram.ext import (CallbackQueryHandler, Updater, MessageHandler,
                          CommandHandler, ConversationHandler, Filters)
from telegram.utils.request import Request
from loguru import logger

dotenv_path = os.path.join(Path(__file__).parent, 'config/.env')
load_dotenv(dotenv_path)

logger.add(
    "logs/info.log",
    format="{time} {level} {message}",
    level="DEBUG",
    rotation="100 MB",
    compression="zip",
)

TOKEN = os.getenv("TOKEN")

@logger.catch
def main():
    '''Setting up all needed to launch bot'''
    logger.info('Started')

    req = Request(
        connect_timeout=30.0,
        read_timeout=5.0,
        con_pool_size=8,
    )
    bot = Bot(
        token=TOKEN,
        request=req,
    )
    updater = Updater(
        bot=bot,
        use_context=True,
    )

    # Проверить что бот корректно подключился к Telegram API
    info = bot.get_me()
    logger.info('Bot info: %s', info)

    # Навесить обработчики команд
    updater.dispatcher.add_handler(CommandHandler('start', checker.greetings_handler))
    updater.dispatcher.add_handler(CallbackQueryHandler(checker.check_handler,
                                            pattern=r'^check$',
                                            pass_user_data=True))
    updater.dispatcher.add_handler(MessageHandler(Filters.all, checker.greetings_handler))

    updater.start_polling()
    updater.idle()
    logger.info('Stopped')

if __name__ == '__main__':
    main()