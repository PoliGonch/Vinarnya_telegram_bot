<h1>DjangoWineBot</h1>

DjangoWineBot is a project that helps to collect your private wine catalog.
You add wine photos via Telegram bot and check, whether you liked the wine or not.

You may use the bot to:
1. Add photo of the wine you liked or didn't like.
2. View wines that you've added (filter them by your opinion - like or dislike, color, type or country).
3. Get random wine and a link to buy it online in a local store.

<h3>How to run the project</h3>

1. Create .env file in the root directory and add you Telegrambot token and PostgreSQL login/password to it. 
2. You need docker and docker-compose to be installed. Use command "docker-compose up". 
3. Run the bot by "./manage.py telebot" command. 
4. Not necessary: Use command "celery -A DjangoWineBot worker -B  --loglevel=info" to run celery task. It sends a reminder to bot users every Saturday.