from telebot import types

from telegram_bot import message_text
from telegram_bot.states.base import BaseState
from vinarnya.models import Language, User


class Hello(BaseState):
    text_wo_lang = 'Choose language | Оберіть мову:'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.user.language is not None:
            self.language = message_text.str_to_class(self.user.language.name)

    def display_start(self):
        return self.bot.send_message(self.chat_id, self.get_start_msg_text(), reply_markup=self.get_keyboard())

    def get_start_msg_text(self):
        if self.user.language is None:
            return self.text_wo_lang
        self.language = message_text.str_to_class(self.user.language.name)
        return self.language.hello_msg

    def get_msg_text(self):
        self.language = message_text.str_to_class(self.user.language.name)
        return self.language.hello_continue_msg

    def get_keyboard(self):
        keyboard = types.InlineKeyboardMarkup()
        if self.user.language is None:
            keyboard.add(
                types.InlineKeyboardButton(text='English', callback_data='setlang:En'),
                types.InlineKeyboardButton(text='Українська', callback_data='setlang:Uk')
            )
        else:
            self.language = message_text.str_to_class(self.user.language.name)
            keyboard.add(types.InlineKeyboardButton(text=self.language.add_wine, callback_data='nextstate:AddWine'))
            keyboard.add(types.InlineKeyboardButton(text=self.language.show_wine, callback_data='nextstate:ShowWine'))
            keyboard.add(types.InlineKeyboardButton(text=self.language.random_wine, callback_data='nextstate:RandomWine'))
        return keyboard

    #
    def process_call_back(self, message: types.CallbackQuery) -> 'BaseState':
        if message.data and message.data.split(':')[0] == 'setlang':
            language = message.data.split(':')[1]
            self.user.language, _ = Language.objects.get_or_create(name=language, )
            self.user.save()
            return self

        if message.data and message.data == 'nextstate:AddWine':
            from telegram_bot.states.bot_add_wine_state import AddWineState
            self.user.user_state = 'AddWineState'
            self.user.save()
            return AddWineState(self.bot, self.user, self.msg_to_del)

        if message.data and message.data == 'nextstate:ShowWine':
            from telegram_bot.states.bot_show_wine_state import ShowWineState
            self.user.user_state = 'ShowWineState'
            self.user.save()
            return ShowWineState(self.bot, self.user, self.msg_to_del)

        if message.data and message.data == 'nextstate:RandomWine':
            from telegram_bot.states.bot_random_wine_state import RandomWineState
            self.user.user_state = 'RandomWineState'
            self.user.save()
            return RandomWineState(self.bot, self.user, self.msg_to_del)

    def change_lang(self, message: types.Message):
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(
            types.InlineKeyboardButton(text='English', callback_data='setlang:En'),
            types.InlineKeyboardButton(text='Українська', callback_data='setlang:Uk')
        )
        self.bot.send_message(self.chat_id, self.text_wo_lang, reply_markup=keyboard)

