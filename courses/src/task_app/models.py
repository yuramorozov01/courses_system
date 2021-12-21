from base_app.utils import get_unique_filename
from django.contrib.auth import get_user_model
from django.db import models


class TaskStatement(models.Model):
    '''Task statement model.
    Teacher of course can add task statement to the lecture.
    '''

    lecture = models.ForeignKey(
        'lecture_app.Lecture',
        verbose_name='Lecture',
        on_delete=models.CASCADE,
        related_name='task_statements'
    )
    title = models.CharField('Title', max_length=128)
    text = models.TextField('Text', max_length=8192)
    author = models.ForeignKey(
        get_user_model(),
        verbose_name='Author',
        on_delete=models.CASCADE,
        related_name='own_task_statements'
    )
    created_at = models.DateTimeField('Creation time', auto_now_add=True)

    class Meta:
        verbose_name = 'Task statement'
        verbose_name_plural = 'Task statements'

    def __str__(self):
        return self.title


class TaskStatementFile(models.Model):
    '''Task statement file model.
    Attached files to a task statement.
    '''

    task_statement = models.ForeignKey(
        TaskStatement,
        verbose_name='Task statement',
        on_delete=models.CASCADE,
        related_name='files'
    )
    file = models.FileField('File', upload_to=get_unique_filename)
    author = models.ForeignKey(
        get_user_model(),
        verbose_name='Author',
        on_delete=models.CASCADE,
        related_name='own_task_statement_files'
    )

    class Meta:
        verbose_name = 'Task statement file'
        verbose_name_plural = 'Task statement files'

    def __str__(self):
        return f'{self.author.username} | {self.file.path}'


class Task(models.Model):
    '''Completed task model.
    Students can send task attached to a task statement.
    '''

    task_statement = models.ForeignKey(
        TaskStatement,
        verbose_name='Task statement',
        on_delete=models.CASCADE,
        related_name='tasks'
    )
    text = models.TextField('Text', blank=True, max_length=8192)
    link = models.URLField('Link', null=True, blank=True)
    author = models.ForeignKey(
        get_user_model(),
        verbose_name='Author',
        on_delete=models.CASCADE,
        related_name='own_tasks'
    )
    created_at = models.DateTimeField('Creation time', auto_now_add=True)

    class Meta:
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'

    def __str__(self):
        return f'{self.author.username} | {self.created_at}'


class TaskFile(models.Model):
    '''Task file model.
    Attached files to a task.
    '''

    task = models.ForeignKey(
        Task,
        verbose_name='Task',
        on_delete=models.CASCADE,
        related_name='files'
    )
    file = models.FileField('File', upload_to=get_unique_filename)
    author = models.ForeignKey(
        get_user_model(),
        verbose_name='Author',
        on_delete=models.CASCADE,
        related_name='own_task_files'
    )

    class Meta:
        verbose_name = 'Task file'
        verbose_name_plural = 'Task files'

    def __str__(self):
        return f'{self.author.username} | {self.file.path}'
