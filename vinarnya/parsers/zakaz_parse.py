import logging
from vinarnya.parsers.zakaz_ua import Zakaz

logger = logging.getLogger()

def zakaz_parse(search_type=None, search_color=None, store_name=None):
    parser = Zakaz(search_type, search_color, store_name)
    return parser.search_wine()


def zakaz_parse_celery(search_type=None, search_color=None, store_name='Novus'):
    parser = Zakaz(search_type, search_color, store_name)
    return parser.search_wine()
