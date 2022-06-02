import os
from celery.schedules import crontab
from celery import Celery

# Set the default Django settings module for the 'celery' program.
from celery.signals import worker_ready

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoWineBot.settings')

app = Celery('DjangoWineBot')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


app.conf.beat_schedule = {
    # Executes every Friday evening.
    'add-every-friday-evening': {
        'task': 'vinarnya.tasks.send_drink_reminder',
        'schedule': crontab(hour=17, minute=30, day_of_week=7),
        'args': (),
    },
}
