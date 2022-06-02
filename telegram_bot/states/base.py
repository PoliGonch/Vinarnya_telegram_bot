import telebot
from telebot import types


class BaseState:
    text = ''

    def __init__(self, bot:telebot.TeleBot, user, msg_to_del=None, view_liked=None):
        self.bot = bot
        self.chat_id = user.chat_id
        self.user = user
        self.msg_to_del = msg_to_del
        self.view_liked = view_liked


    def display(self):
        if self.msg_to_del:
            self.bot.delete_message(chat_id=self.chat_id, message_id=self.msg_to_del)
        return self.bot.send_message(self.chat_id, self.get_msg_text(), reply_markup=self.get_keyboard())

    def get_msg_text(self):
        return self.text

    def get_keyboard(self):
        return None

    def delete_msg_text(self, msg_id):
        self.msg_to_del = msg_id

    def process_photo_message(self, message):
        return self

    def send_warning(self, text):
        self.bot.send_message(self.chat_id, text)

    def process_call_back(self, message: types.CallbackQuery) -> 'BaseState':
        return self

    def process_text_message(self, message: types.Message) -> 'BaseState':
        return self