import os
from pythonping import ping
from pathlib import Path
from telegram import (InlineKeyboardButton, InlineKeyboardMarkup, Update,
                      ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton)
from telegram.ext import CallbackContext, ConversationHandler
from loguru import logger
from dotenv import load_dotenv


dotenv_path = os.path.join(Path(__file__).parent, 'config/.env')
load_dotenv(dotenv_path)

IP = os.getenv("IP")


def ping_test(host):
    try:
        ping_test = ping(host, verbose=True, size=1)
        logger.info(ping_test)
        return True
    except:
        return False
               

def greetings_handler(update: Update, context: CallbackContext):
    inline_keyboard = [
        [
            InlineKeyboardButton(text='Варюш, свет есть?',
                                 callback_data='check')
        ],
    ]
    inline_buttons = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
    context.bot.send_message(chat_id=update.message.from_user.id,
                            text='Родители, вы всегда можете у меня спросить есть ли свет дома.',
                            reply_markup=inline_buttons)
    return ConversationHandler.END       


def check_handler(update: Update, context: CallbackContext):
    inline_keyboard = [
        [
            InlineKeyboardButton(text='Варюш, свет есть?',
                                 callback_data='check')
        ],
    ]
    inline_buttons = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
    result = ping_test(IP)
    if result:
        context.bot.send_sticker(chat_id=update.callback_query.message.chat.id,
                                sticker='CAACAgIAAxkBAAMFY69KYksBvI17ZEdBcYj8X2yij84AAsEdAAJDwjlJEyPqj8svtrUtBA')
        context.bot.send_message(chat_id=update.callback_query.message.chat.id,
                                text='Все на месте, что-то еще?',
                                reply_markup=inline_buttons)                                #If ping test is 0, it' reachable
        logger.info('Reachable')
    else:
        context.bot.send_sticker(chat_id=update.callback_query.message.chat.id,
                                sticker='CAACAgIAAxkBAAMJY69MZagC1Rr8K7oY8gNnHfAvKRIAAjYcAAKdMBhJ-oBMgz54EIctBA')
        context.bot.send_message(chat_id=update.callback_query.message.chat.id,
                                text='Очень жаль, что-то еще?',
                                reply_markup=inline_buttons)
        logger.info('Not Reachable')
    return ConversationHandler.END                            #Else, it's not reachable

if __name__ == '__main__':
    ping_test('85.209.45.169')