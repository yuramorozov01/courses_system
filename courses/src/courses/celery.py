import os

from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'courses.settings')

app = Celery('courses')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

# Create scheduled tasks
app.conf.beat_schedule = {
    # Executes daily at midnight
    'daily-at-midnight-send-unreviewed-tasks': {
        'task': 'task_app.tasks.SendEmailWithUnreviewedTasksTask',
        'schedule': crontab(minute=0, hour=0),
        # 'schedule': crontab(minute='*/1'),
        'options': {'queue': 'email', 'priority': 5},
    },
    'calc-amount-of-students-every-5-min': {
        'task': 'course_app.tasks.CalcAmountOfStudentsInCourseTask',
        'schedule': crontab(minute='*/5'),
        # 'schedule': crontab(minute='*/1'),
        'options': {'queue': 'default'},
    }
}


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
