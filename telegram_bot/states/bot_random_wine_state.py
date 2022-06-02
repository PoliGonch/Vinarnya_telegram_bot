from telebot import types

from telegram_bot import message_text
from telegram_bot.states.base import BaseState
from telegram_bot.states.hello_state import Hello
from telegram_bot.states.bot_random_color_state import RandomColorState
from telegram_bot.states.bot_random_type_state import RandomTypeState
from vinarnya.parsers.zakaz_parse import zakaz_parse


class RandomWineState(BaseState):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.language = message_text.str_to_class(self.user.language.name)

        self.back_button = types.InlineKeyboardButton(text=self.language.back, callback_data='nextstate:Hello')

    def get_msg_text(self):
        return self.language.choose_random

    def get_keyboard(self):
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text=self.language.random_random, callback_data='chooserandom:Random'),
                     types.InlineKeyboardButton(text=self.language.random_type, callback_data='nextstate:RandomType'),
                     types.InlineKeyboardButton(text=self.language.random_color, callback_data='nextstate:RandomColor'))
        keyboard.add(self.back_button)
        return keyboard

    def process_call_back(self, message: types.CallbackQuery) -> 'BaseState':

        if message.data and message.data == 'chooserandom:Random':
            wine = zakaz_parse(store_name='Novus')
            self.bot.send_message(self.chat_id,
                                  f'{self.language.try_this} {wine["title"]}, {self.language.try_this_2} {wine["price"]} {self.language.currency}. '
                                  f'{wine["link"]}')
            self.user.user_state = 'Hello'
            self.user.save()
            return Hello(self.bot, self.user, self.msg_to_del)

        if message.data and message.data == 'nextstate:RandomType':
            self.user.user_state = 'RandomTypeState'
            self.user.save()
            return RandomTypeState(self.bot, self.user, self.msg_to_del)

        if message.data and message.data == 'nextstate:RandomColor':
            self.user.user_state = 'RandomColorState'
            self.user.save()
            return RandomColorState(self.bot, self.user, self.msg_to_del)

        if message.data and message.data == 'nextstate:Hello':
            self.user.user_state = 'Hello'
            self.user.save()
            return Hello(self.bot, self.user, self.msg_to_del)
