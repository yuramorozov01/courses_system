from celery import Task
from courses.celery import app
from django.conf import settings
from django.core.mail import send_mail


class SendNewMarkEmailTask(Task):
    name = 'send-new-mark-email'

    def run(self, email, mark_author_username, task_statement_title, mark_value, *args, **kwargs):
        send_mail(
            'Teacher added mark to your task "{}"'.format(task_statement_title),
            'Task statement title: {}\nTeacher: {}\nMark value: {}'.format(
                task_statement_title,
                mark_author_username,
                mark_value
            ),
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )
        return True


app.register_task(SendNewMarkEmailTask)
