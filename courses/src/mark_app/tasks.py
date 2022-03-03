from celery import shared_task
from decouple import config
from django.core.mail import send_mail


@shared_task
def send_new_mark_email(email, mark_author_username, task_statement_title, mark_value):
    send_mail(
        'Teacher added mark to your task "{}"'.format(task_statement_title),
        'Task statement title: {}\nTeacher: {}\nMark value: {}'.format(
            task_statement_title,
            mark_author_username,
            mark_value
        ),
        config('EMAIL_HOST_USER'),
        [email],
        fail_silently=False,
    )
    return True
