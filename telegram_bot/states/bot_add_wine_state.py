from pathlib import Path

from telebot import types

from telegram_bot import message_text
from telegram_bot.states.base import BaseState
from telegram_bot.states.hello_state import Hello
from vinarnya.models import Color, Type, Country, Wine


class AddWineState(BaseState):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.language = message_text.str_to_class(self.user.language.name)

        self.color = None
        self.type = None
        self.country = None
        self.image = None

        self.title = None

        self.back_button = types.InlineKeyboardButton(text=self.language.back, callback_data='nextstate:Hello')

        self.filter_variants = [
            (self.language.add_wine_photo,
             []),

            (self.language.like,
             [types.InlineKeyboardButton(text=self.language.yes, callback_data='setlike:Like'),
              types.InlineKeyboardButton(text=self.language.no, callback_data='setlike:Dislike')]),

            (self.language.additional_info,
             [types.InlineKeyboardButton(text=self.language.yes, callback_data='addinfo:Yes'),
              types.InlineKeyboardButton(text=self.language.no, callback_data='addinfo:No')]),

            (self.language.choose_wine_color,
             [types.InlineKeyboardButton(text=value,
                                         callback_data=f'setcolor:{key}') for key, value in
              self.language.color_dict.items()]),

            (self.language.choose_wine_type,
             [types.InlineKeyboardButton(text=value,
                                         callback_data=f'settype:{key}') for key, value in
              self.language.type_dict.items()]),

            (self.language.choose_wine_country,
             [types.InlineKeyboardButton(text=value,
                                         callback_data=f'setcountry:{key}') for key, value in
              self.language.country_dict.items()])
        ]

    def display(self):
        if not self.filter_variants:
            self.save_wine()
        return super().display()

    def get_msg_text(self):
        if self.filter_variants:
            return self.filter_variants[0][0]
        return self.language.well_done_msg

    def get_keyboard(self):
        keyboard = types.InlineKeyboardMarkup()
        if self.filter_variants:
            keyboard.add(*self.filter_variants[0][1])
            keyboard.add(self.back_button)
        else:
            keyboard.add(types.InlineKeyboardButton(text=self.language.continue_chat, callback_data='nextstate:Hello'))
        return keyboard

    def process_call_back(self, message: types.CallbackQuery) -> 'BaseState':
        if self.filter_variants:
            self.filter_variants.pop(0)

        if message.data and message.data == 'setlike:Like':
            return self.set_like()

        if message.data and message.data == 'setlike:Dislike':
            return self.set_dislike()

        if message.data and message.data == 'addinfo:Yes':
            return self

        if message.data and message.data == 'addinfo:No':
            self.filter_variants = []
            self.save_wine()
            return self

        if message.data and message.data.split(':')[0] == 'setcolor':
            color = message.data.split(':')[1]
            return self.set_color(color)

        if message.data and message.data.split(':')[0] == 'settype':
            wine_type = message.data.split(':')[1]
            return self.set_type(wine_type)

        if message.data and message.data.split(':')[0] == 'setcountry':
            country = message.data.split(':')[1]
            return self.set_country(country)

        if message.data and message.data == 'nextstate:Hello':
            self.user.user_state = 'Hello'
            self.user.save()
            return Hello(self.bot, self.user, self.msg_to_del)

    def set_like(self):
        self.like = True
        return self

    def set_dislike(self):
        self.like = False
        return self

    def set_color(self, color):
        self.color = color
        return self

    def set_type(self, wine_type):
        self.type = wine_type
        return self

    def set_country(self, country):
        self.country = country
        return self

    def save_wine(self):
        if self.color:
            self.color, _ = Color.objects.get_or_create(name_en=self.color)

        if self.type:
            self.type, _ = Type.objects.get_or_create(name_en=self.type)

        if self.country:
            self.country, _ = Country.objects.get_or_create(name_en=self.country)

        wine, _ = Wine.objects.get_or_create(liked=self.like,
                                             image=self.image_name,
                                             image_id=self.image_id,
                                             color=self.color,
                                             type=self.type,
                                             country=self.country,
                                             name=self.title,
                                             user=self.user)
        wine.save()
        return self

    def process_photo_message(self, message: types.Message):
        if self.image:
            return self

        if self.filter_variants:
            self.filter_variants.pop(0)

        file_id = message.photo[-1].file_id
        file_info = self.bot.get_file(file_id)
        downloaded_file = self.bot.download_file(file_info.file_path)

        user_dir = f"media/user_{self.chat_id}"
        Path(user_dir).mkdir(parents=True, exist_ok=True)

        with open(f'{user_dir}/image_{self.chat_id}{message.message_id}.jpg', 'wb') as new_file:
            new_file.write(downloaded_file)

        self.image = True
        self.image_id = file_id
        self.image_name = f'{user_dir}/image_{self.chat_id}{message.message_id}.jpg'
        self.bot.delete_message(self.chat_id, message.message_id, 5)
        self.bot.send_photo(self.chat_id, open(f'{user_dir}/image_{self.chat_id}{message.message_id}.jpg', 'rb'),
                            self.language.wine_photo)

        return self