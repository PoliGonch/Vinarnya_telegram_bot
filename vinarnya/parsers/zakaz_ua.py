import json
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
# from time import strptime, strftime
from datetime import datetime
import random

import requests
from bs4 import BeautifulSoup


class Zakaz:
    BASE_URL = 'https://stores-api.zakaz.ua/stores/'

    def __init__(self, search_type=None, search_color=None, store_name=None):
        self.search_type = search_type
        self.search_color = search_color
        self.store_name = store_name

        self.store_dict = {
            'Kosmos': '48225531',
            'Novus': '48201070',
            'MegaMarket': '48267601'
        }

    def search_wine(self):
        if self.store_name:
            store = getattr(sys.modules[__name__], self.store_name)
            return store(self.search_type, self.search_color, self.store_name).search_wine()


class Novus(Zakaz):
    BASE_URL = 'https://stores-api.zakaz.ua/stores/48201070/categories/'
    wine_total = 'wine/'

    wine_types = {
        'Dry': 'dry-wine/',
        'Semi-sweet': 'semi-sweet-wine/',
        'Sweet': 'dessert-wine/',
        'Sparkling': 'champagne-sparkling-wine/'
    }
    wine_colors = {
        'Red': 'red',
        'White': 'white',
        'Rose': 'pink',
        'Other': 'orange'
    }

    params = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def search_wine(self):
        if self.search_type:
            category_name = self.wine_types[f'{self.search_type}']
        else:
            category_name = self.wine_total
            if self.search_color:
                self.params['color'] = self.wine_colors[f'{self.search_color}']
                # print(f'{self.params=}')
        resp = requests.get(self.BASE_URL + category_name + 'products', params=self.params)
        bs = BeautifulSoup(resp.text, 'lxml')
        site_json = json.loads(bs.text)
        number = random.randint(0, len(site_json['results']) - 1)

        link = site_json["results"][number]["web_url"]
        wine_title = site_json["results"][number]["title"]
        raw_price = str(site_json["results"][number]["price"])
        wine_price = raw_price[:-2]
        return {'title': wine_title, 'price': wine_price, 'color': self.search_color, 'link': link}



