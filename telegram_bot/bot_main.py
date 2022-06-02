import logging

from dotenv import load_dotenv

import os
import telebot

import vinarnya.models
from telegram_bot import message_text
from telegram_bot.states.base import BaseState
from telegram_bot.states.hello_state import Hello
from vinarnya.models import User, Wine

load_dotenv()

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

bot = telebot.TeleBot(os.getenv('TELEGRAM_TOKEN'))
clients: dict = {}


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message: telebot.types.Message):
    user, _ = User.objects.get_or_create(chat_id=message.chat.id, defaults={'language': None, 'user_state': None})
    bot_new = Hello(bot, user)
    bot_new.display_start()
    clients[message.chat.id] = bot_new


@bot.message_handler(commands=['language'])
def change_language(message: telebot.types.Message):
    user, _ = User.objects.get_or_create(chat_id=message.chat.id, defaults={'language': None, 'user_state': 'Hello'})
    bot_new = Hello(bot, user)
    bot_new.change_lang(message)
    clients[message.chat.id] = bot_new


@bot.callback_query_handler(func=lambda message: True)
def process_call_back(message: telebot.types.CallbackQuery):
    chat_id = message.from_user.id
    bot.answer_callback_query(callback_query_id=message.id)
    new_state_class = get_state(chat_id).process_call_back(message)
    clients[chat_id] = new_state_class
    display(chat_id)


@bot.message_handler(func=lambda message: True)
def echo_all(message: telebot.types.Message):
    chat_id = message.chat.id
    new_state_class = get_state(chat_id).process_text_message(message)
    clients[chat_id] = new_state_class
    display(chat_id)


@bot.message_handler(content_types=['photo'])
def photo(message: telebot.types.Message):
    chat_id = message.chat.id
    new_state_class = get_state(chat_id).process_photo_message(message)
    clients[chat_id] = new_state_class
    display(chat_id)


def display(chat_id):
    state = get_state(chat_id)
    prev_msg = state.display()
    state.delete_msg_text(msg_id=prev_msg.message_id)


def get_state(chat_id) -> BaseState:
    try:
        return clients[chat_id]
    except KeyError:
        user, _ = User.objects.get_or_create(chat_id=chat_id, defaults={'language': None, 'user_state': 'Hello'})
        state_name = user.user_state
        state = message_text.str_to_class(state_name)
        return state(bot, user)
