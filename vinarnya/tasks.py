import logging
import traceback
from datetime import datetime

from django.db import IntegrityError
from django.http import HttpRequest
from django.urls import reverse, get_script_prefix

from DjangoWineBot.celery import app
from telegram_bot import bot_main, message_text
from vinarnya.models import User
from vinarnya.parsers.zakaz_parse import zakaz_parse_celery

logger = logging.getLogger()


@app.task()
def store_statistic():
    logger.info("all ok")


@app.task()
def send_drink_reminder():
    wine = zakaz_parse_celery()
    logger.info(f'Got wine: {wine}')
    users = User.objects.all()

    for user in users:
        lang = message_text.str_to_class(user.language.name)
        msg_text = f'{lang.drink_reminder}{wine["title"]}, {lang.try_this_2} {wine["price"]} {lang.currency}'

        send_news_to_subscriber.delay(user.chat_id, msg_text)


@app.task()
def send_news_to_subscriber(chat_id, msg):
    bot_main.bot.send_message(chat_id, msg)


@app.task()
def start_bot():
    bot_main.bot.infinity_polling()

app.conf.timezone = 'UTC'