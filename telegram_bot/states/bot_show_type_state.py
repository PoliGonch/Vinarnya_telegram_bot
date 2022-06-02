from django.shortcuts import get_object_or_404
from telebot import types

from telegram_bot import message_text
from telegram_bot.states.base import BaseState
from telegram_bot.states.hello_state import Hello
from vinarnya.models import Wine, Type


class ShowTypeState(BaseState):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.language = message_text.str_to_class(self.user.language.name)

        self.back_button = types.InlineKeyboardButton(text=self.language.back, callback_data='nextstate:Hello')

    def get_msg_text(self):
        return self.language.choose_type_to_show

    def get_keyboard(self):
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(*[types.InlineKeyboardButton(text=value, callback_data=f'showtype:{key}') for key, value in
                       self.language.type_dict.items()])
        keyboard.add(self.back_button)
        return keyboard

    def process_call_back(self, message: types.CallbackQuery) -> 'BaseState':
        if message.data and message.data.split(':')[0] == 'showtype':
            type_name = message.data.split(':')[1]
            self.show_wines(type_name)
            self.user.user_state = 'Hello'
            self.user.save()
            return Hello(self.bot, self.user, self.msg_to_del)

        if message.data and message.data == 'nextstate:Hello':
            self.user.user_state = 'Hello'
            self.user.save()
            return Hello(self.bot, self.user, self.msg_to_del)

    def show_wines(self, type_name):
        wine_list = self.get_wines(type_name)
        if wine_list:
            for wine in wine_list:
                if wine.liked == True:
                    photo_text = self.language.you_liked
                else:
                    photo_text = self.language.you_disliked
                self.bot.send_photo(self.chat_id, wine.image_id, photo_text)
            return self.bot.send_message(self.chat_id,
                                         f'{self.language.show_by_type_text}{self.language.type_dict[type_name]}')
        return self.bot.send_message(self.chat_id, self.language.no_wines_found)

    def get_wines(self, type_name) -> list[Wine]:
        if Wine.objects.filter(user=self.user).exists():
            wine_type = get_object_or_404(Type, name_en=type_name)
            if wine_type:
                return [*Wine.objects.filter(user=self.user, type=wine_type)]
        return []