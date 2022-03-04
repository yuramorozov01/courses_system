from celery import shared_task
from decouple import config
from django.core.mail import send_mail
from task_app.models import Task


@shared_task
def send_email_with_unreviewed_tasks():
    unreviewed_tasks = Task.objects.filter(mark=None).prefetch_related(
        'task_statement',
        'task_statement__lecture',
        'task_statement__lecture__course',
        'task_statement__lecture__course__teachers'
    )

    # Collect all unreviewed tasks by every teacher of this tasks
    teachers_with_unreviewed_tasks = {}
    for task in unreviewed_tasks:
        for teacher in task.task_statement.lecture.course.teachers.all():
            to_review_tasks = teachers_with_unreviewed_tasks.get(teacher, [])
            to_review_tasks.append(task)
            teachers_with_unreviewed_tasks[teacher] = to_review_tasks

    # Send email to every teacher with unreviewed tasks
    for teacher, tasks in teachers_with_unreviewed_tasks.items():
        if hasattr(teacher, 'email'):
            subject = 'You have {} unreviewed tasks'.format(len(tasks))
            message = ''
            for task in tasks:
                message += 'Course: {} | Task statement: {} | Task author: {} | Link: {}\n'.format(
                    task.task_statement.lecture.course.title,
                    task.task_statement.title,
                    task.author.username,
                    task.get_absolute_url()
                )
            send_mail(
                subject,
                message,
                config('EMAIL_HOST_USER'),
                [teacher.email],
                fail_silently=False,
            )
    return True
