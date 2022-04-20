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
    'daily_at_midnight_send_unreviewed_tasks': {
        'task': 'task_app.tasks.SendEmailWithUnreviewedTasksTask',
        'schedule': crontab(minute=0, hour=0),
    },
    'calc_amount_of_students_every_5_min': {
        'task': 'course_app.tasks.CalcAmountOfStudentsInCourseTask',
        'schedule': crontab(minute='*/5'),
    },
    'daily_at_midnight_capture_money_on_started_courses': {
        'task': 'payments_app.tasks.CaptureStartedCoursesTask',
        'schedule': crontab(minute=0, hour=0),
    }
}

app.conf.task_routes = {
    'task_app.tasks.SendEmailWithUnreviewedTasksTask': {
        'queue': 'email',
        'priority': 5,
    },
    'course_app.tasks.CalcAmountOfStudentsInCourseTask': {
        'queue': 'default',
        'priority': 8,
    },
    'payments_app.tasks.CaptureStartedCoursesTask': {
        'queue': 'default',
        'priority': 1,
    },
    'send_new_mark_email': {
        'queue': 'email',
        'priority': 2,
    },
}


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
