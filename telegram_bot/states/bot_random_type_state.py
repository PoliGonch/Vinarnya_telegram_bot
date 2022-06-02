from telebot import types

from telegram_bot import message_text
from telegram_bot.states.base import BaseState
from telegram_bot.states.hello_state import Hello
from vinarnya.parsers.zakaz_parse import zakaz_parse


class RandomTypeState(BaseState):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.language = message_text.str_to_class(self.user.language.name)
        self.back_button = types.InlineKeyboardButton(text=self.language.back, callback_data='nextstate:Hello')

    def get_msg_text(self):
        return self.language.choose_type_to_show

    def get_keyboard(self):
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(*[types.InlineKeyboardButton(text=value, callback_data=f'randomtype:{key}') for key, value in
                       self.language.type_dict.items()])
        keyboard.add(self.back_button)
        return keyboard

    def process_call_back(self, message: types.CallbackQuery) -> 'BaseState':

        if message.data and message.data.split(":")[0] == 'randomtype':
            random_type = message.data.split(":")[-1]
            wine = zakaz_parse(search_type=random_type, store_name='Novus')
            self.bot.send_message(self.chat_id,
                                  f'{self.language.try_this} {wine["title"]}, {self.language.try_this_2} {wine["price"]} {self.language.currency}. '
                                  f'{wine["link"]}')
            self.user.user_state = 'Hello'
            self.user.save()
            return Hello(self.bot, self.user, self.msg_to_del)

        if message.data and message.data == 'nextstate:Hello':
            self.user.user_state = 'Hello'
            self.user.save()
            return Hello(self.bot, self.user, self.msg_to_del)