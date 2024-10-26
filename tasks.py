from celery import Celery
from datetime import timedelta
from celery.schedules import schedule


app = Celery('tasks', broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')


@app.task
def print_message():
    print("Salom, Musharraf")


app.conf.beat_schedule = {
    'print-every-3-seconds': {
        'task': 'tasks.print_message',
        'schedule': schedule(run_every=timedelta(seconds=3)),  # Har 3 soniyada bajariladi
    },
}

app.conf.timezone = 'Asia/Tashkent'
