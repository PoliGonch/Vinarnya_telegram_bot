from telebot import types

from telegram_bot import message_text
from telegram_bot.states.base import BaseState
from telegram_bot.states.hello_state import Hello
from vinarnya.models import Wine


class ShowLikeState(BaseState):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.language = message_text.str_to_class(self.user.language.name)

    def display(self):
        wine_list = self.get_wines()
        if self.view_liked:
            msg = self.language.show_wine_liked_text
        else:
            msg = self.language.show_wine_disliked_text
        if len(wine_list) > 0:
            for wine in wine_list:
                self.bot.send_photo(self.chat_id, wine.image_id)
            return self.bot.send_message(self.chat_id, msg, reply_markup=self.get_keyboard())
        return self.bot.send_message(self.chat_id, self.language.no_wines_found, reply_markup=self.get_keyboard())

    def get_keyboard(self):
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text=self.language.continue_chat, callback_data='nextstate:Hello'))
        return keyboard

    def process_call_back(self, message: types.CallbackQuery) -> 'BaseState':
        if message.data and message.data == 'nextstate:Hello':
            self.user.user_state = 'Hello'
            self.user.save()
            return Hello(self.bot, self.user, self.msg_to_del)

    def get_wines(self) -> list[Wine]:
        if Wine.objects.filter(user=self.user).exists():
            return [*Wine.objects.filter(user=self.user, liked=self.view_liked).order_by('id')]
        return []