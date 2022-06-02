import datetime
import sys
from datetime import datetime
import pytz
from IPython.utils.tz import utcnow

from telegram_bot.states.bot_add_wine_state import AddWineState
from telegram_bot.states.bot_random_color_state import RandomColorState
from telegram_bot.states.bot_random_type_state import RandomTypeState
from telegram_bot.states.bot_random_wine_state import RandomWineState
from telegram_bot.states.bot_show_color_state import ShowColorState
from telegram_bot.states.bot_show_country_state import ShowCountryState
from telegram_bot.states.bot_show_wine_state import ShowWineState
from telegram_bot.states.hello_state import Hello
from telegram_bot.states.bot_show_like_state import ShowLikeState
from telegram_bot.states.bot_show_type_state import ShowTypeState
from vinarnya.models import Language, User, Wine, Color, Country, Type

def get_time():
    now = datetime.now(pytz.timezone('Etc/GMT-3'))
    return now.strftime("%H:%M")

class En:
    hello_msg = "Hi! I'm your private winery. You can add wines you like or dislike. Choose what you want to do:"
    hello_continue_msg = "Choose what you want to do:"

    # standart answears
    back = 'Back to menu'
    yes = "Yes"
    no = "No"
    other = "Other"
    skip = "Skip"

    # Hello msgs
    add_wine = "Add wine"
    show_wine = "View my wines"
    random_wine = "Get random wine 🍷"

    # AddWine msgs
    add_wine_photo = "Please send me a photo of the bottle. Make sure the wine label is visible"
    wine_photo = "I'll add this photo 🔥"

    like = "Did you like this wine?"

    additional_info = "Do you want to add some additional info?"

    choose_wine_color = "Choose wine color:"
    choose_wine_type = "Choose wine type:"
    choose_wine_country = "Please choose the country or text it in the field"

    well_done_msg = "Wow! I have added this wine"
    continue_chat = "Continue"

    # ShowWine msgs
    choose_wines_to_show = "Choose wines to show"
    show_all_liked = "All liked"
    show_all_disliked = "All disliked"
    show_by_color = "Choose by color"
    show_by_type = "Choose by type"
    show_by_country = "Choose by country"

    no_wines_found = "Sorry, I haven't found anything. Try again"
    you_liked = "Liked"
    you_disliked = "Disliked"

    # ShowLikeWine msgs
    show_wine_liked_text = "These are wines you liked 🔥"
    show_wine_disliked_text = "These are wines you didn't like"

    # ShowColorWine msgs
    choose_color_to_show = "Choose the color: "
    show_by_color_text = "These are wines by color: "


    # ShowTypeWine msgs
    choose_type_to_show = "Choose the type:"
    show_by_type_text = "These are wines by type: "

    # ShowCountryWine msgs
    choose_country_to_show = "Choose the type:"
    show_by_country_text = "These are wines by country: "

    # RandomWineState msgs
    choose_random = "Choose which wine you want:"

    random_random = "Random"
    random_color = "Choose color"
    random_type = "Choose type"

    try_this = "Try this wine: "
    try_this_2 = "price:"
    currency = "UAH"
    try_this_color = "color:"

    drink_reminder = f"Hi! It's {get_time()}, so it's a great time to have a drink 👌. Why don't you try this: "


    color_dict = {
        f'{color.name_en}': f'{color.name_en}' for color in Color.objects.all()
    }

    type_dict = {
        f'{type.name_en}': f'{type.name_en}' for type in Type.objects.all()
    }

    country_dict = {
        f'{country.name_en}': f'{country.name_en}' for country in Country.objects.all()
    }

class Uk:
    hello_msg = "Вітаю! Це твоя приватна винарня. Тут можеш додавати вина, що тобі до вподоби. Або ж можеш додати ті, що зовсім не смакують, щоб не купити знову. " \
                "Обери, що хочеш зробити:"
    hello_continue_msg = "Обери, що хочеш зробити:"

    # standart answears
    back = 'Назад до меню'
    yes = "Так"
    no = "Ні"
    other = "Інше"
    skip = "Пропустити"

    # Hello msgs
    add_wine = "Додати вино"
    show_wine = "Подивитись мої вина"
    random_wine = "Випадкове вино 🍷"

    # AddWine msgs
    add_wine_photo = "Відправ мені фото пляшки, будь ласка. Переконайся, що етикетку добре видно"
    wine_photo = "Я додам це фото"

    like = "Тобі сподобалось це вино?"

    additional_info = "Хочеш вказати додаткову інформацію?"

    choose_wine_color = "Вкажи колір вина:"
    choose_wine_type = "Вкажи тип вина:"
    choose_wine_country = "Вкажи країну виробника або напиши її в полі нижче"

    continue_chat = "Продовжити"
    well_done_msg = "Супер! Я додав це вино 🔥"

    # ShowWine msgs
    choose_wines_to_show = "Які вина показати?"
    show_all_liked = "Сподобались 😎"
    show_all_disliked = "Не сподобались 💩"
    show_by_color = "За кольором"
    show_by_type = "За типом"
    show_by_country = "За країною"

    no_wines_found = "Вибач, не можу знайти нічого. Спробуй знайти щось інше"
    you_liked = "Сподобалось"
    you_disliked = "Не сподобалось"

    # ShowLikedWine msgs
    show_wine_liked_text = "Це вина, які тобі сподобались 🔥"
    show_wine_disliked_text = "Це вина, що тобі  не сподобались"

    # ShowColorWine msgs
    choose_color_to_show = "Обери колір:"
    show_by_color_text = "Це вина за кольором: "

    # ShowTypeWine msgs
    choose_type_to_show = "Обери тип:"
    show_by_type_text = "Це вина за типом: "

    # ShowCountryWine msgs
    choose_country_to_show = "Обери країну:"
    show_by_country_text = "Це вина за країною: "

    # RandomWineState msgs
    choose_random = "Обери, яке вино хочеш:"

    random_random = "Будь-яке"
    random_color = "Обрати колір"
    random_type = "Обрати тип"

    try_this = "Спробуй це вино:"
    try_this_2 = "ціна:"
    currency = "грн"
    try_this_color = "колір:"

    drink_reminder = f"Привіт! Зараз {get_time()}, а отже це чудова нагода випити вина 👌. Чому б не спробувати це: "

    color_dict = {
        f'{color.name_en}': f'{color.name_uk}' for color in Color.objects.all()
    }

    type_dict = {
        f'{type.name_en}': f'{type.name_uk}' for type in Type.objects.all()
    }

    country_dict = {
        f'{country.name_en}': f'{country.name_uk}' for country in Country.objects.all()
    }

def str_to_class(classname):
    return getattr(sys.modules[__name__], classname)
