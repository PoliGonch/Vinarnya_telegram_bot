from django.shortcuts import get_object_or_404
from telebot import types

from telegram_bot import message_text
from telegram_bot.states.base import BaseState
from telegram_bot.states.hello_state import Hello
from vinarnya.models import Wine, Color, User


class ShowColorState(BaseState):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.language = message_text.str_to_class(self.user.language.name)

        self.back_button = types.InlineKeyboardButton(text=self.language.back, callback_data='nextstate:Hello')

    def get_msg_text(self):
        return self.language.choose_color_to_show

    def get_keyboard(self):
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(*[types.InlineKeyboardButton(text=value, callback_data=f'showcolor:{key}') for key, value in
                       self.language.color_dict.items()])
        keyboard.add(self.back_button)
        return keyboard

    def process_call_back(self, message: types.CallbackQuery) -> 'BaseState':
        if message.data and message.data.split(':')[0] == 'showcolor':
            color_name = message.data.split(':')[1]
            self.show_wines(color_name)
            self.user.user_state = 'Hello'
            self.user.save()
            return Hello(self.bot, self.user, self.msg_to_del)

        if message.data and message.data == 'nextstate:Hello':
            self.user.user_state = 'Hello'
            self.user.save()
            return Hello(self.bot, self.user, self.msg_to_del)

    def show_wines(self, color_name):
        wine_list = self.get_wines(color_name)
        if wine_list:
            for wine in wine_list:
                if wine.liked == True:
                    photo_text = self.language.you_liked
                else:
                    photo_text = self.language.you_disliked
                self.bot.send_photo(self.chat_id, wine.image_id, photo_text)
            return self.bot.send_message(self.chat_id,
                                         f'{self.language.show_by_color_text}{self.language.color_dict[color_name]}')
        return self.bot.send_message(self.chat_id, self.language.no_wines_found)

    def get_wines(self, color_name) -> list[Wine]:
        if Wine.objects.filter(user=self.user).exists():
            color = get_object_or_404(Color, name_en=color_name)
            if color:
                return [*Wine.objects.filter(user=self.user, color=color)]
        return []