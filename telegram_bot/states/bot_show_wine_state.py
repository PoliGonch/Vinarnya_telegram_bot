from telebot import types

from telegram_bot import message_text
from telegram_bot.states.base import BaseState
from telegram_bot.states.hello_state import Hello
from telegram_bot.states.bot_show_country_state import ShowCountryState
from telegram_bot.states.bot_show_type_state import ShowTypeState
from telegram_bot.states.bot_show_color_state import ShowColorState
from telegram_bot.states.bot_show_like_state import ShowLikeState


class ShowWineState(BaseState):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.language = message_text.str_to_class(self.user.language.name)

        self.back_button = types.InlineKeyboardButton(text=self.language.back, callback_data='nextstate:Hello')

        self.filter_variants = [
            (self.language.choose_wines_to_show,
             [types.InlineKeyboardButton(text=self.language.show_all_liked, callback_data='showwine:Like'),
              types.InlineKeyboardButton(text=self.language.show_all_disliked, callback_data='showwine:Dislike'),
              types.InlineKeyboardButton(text=self.language.show_by_color, callback_data='showwine:ByColor'),
              types.InlineKeyboardButton(text=self.language.show_by_type, callback_data='showwine:ByType'),
              types.InlineKeyboardButton(text=self.language.show_by_country, callback_data='showwine:ByCountry')]),
        ]

    def get_msg_text(self):
        if self.filter_variants:
            return self.filter_variants[0][0]

    def get_keyboard(self):
        keyboard = types.InlineKeyboardMarkup()
        if self.filter_variants:
            keyboard.add(self.filter_variants[0][1][0], self.filter_variants[0][1][1])
            keyboard.add(self.filter_variants[0][1][2], self.filter_variants[0][1][3], self.filter_variants[0][1][4])
            keyboard.add(self.back_button)
        return keyboard

    def process_call_back(self, message: types.CallbackQuery) -> 'BaseState':
        if self.filter_variants:
            self.filter_variants.pop(0)

        if message.data and message.data == 'showwine:Like':
            self.view_liked = True
            self.user.user_state = 'ShowLikeState'
            self.user.save()
            return ShowLikeState(self.bot, self.user, self.msg_to_del, self.view_liked)

        if message.data and message.data == 'showwine:Dislike':
            self.view_liked = False
            self.user.user_state = 'ShowLikeState'
            self.user.save()
            return ShowLikeState(self.bot, self.user, self.msg_to_del, self.view_liked)

        if message.data and message.data == 'showwine:ByColor':
            self.user.user_state = 'ShowColorState'
            self.user.save()
            return ShowColorState(self.bot, self.user, self.msg_to_del)

        if message.data and message.data == 'showwine:ByType':
            self.user.user_state = 'ShowTypeState'
            self.user.save()
            return ShowTypeState(self.bot, self.user, self.msg_to_del)

        if message.data and message.data == 'showwine:ByCountry':
            self.user.user_state = 'ShowCountryState'
            self.user.save()
            return ShowCountryState(self.bot, self.user, self.msg_to_del)

        if message.data and message.data == 'nextstate:Hello':
            self.user.user_state = 'Hello'
            self.user.save()
            return Hello(self.bot, self.user, self.msg_to_del)