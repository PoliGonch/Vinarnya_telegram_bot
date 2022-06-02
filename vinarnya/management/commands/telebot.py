from django.core.management import BaseCommand
from telegram_bot.bot_main import bot


class Command(BaseCommand):

    def handle(self, *args, **options):
        bot.infinity_polling()
