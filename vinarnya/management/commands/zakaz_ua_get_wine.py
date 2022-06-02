from django.core.management.base import BaseCommand
from vinarnya.parsers.zakaz_parse import zakaz_parse

class Command(BaseCommand):

    def handle(self, *args, **options):
        zakaz_parse(*args, **options)
