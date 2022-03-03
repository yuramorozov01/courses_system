from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Mark(models.Model):
    '''Mark model.
    Teacher of course can add mark to the task.
    The task can have only one mark.
    '''

    task = models.OneToOneField(
        'task_app.Task',
        verbose_name='Task',
        on_delete=models.CASCADE,
        related_name='mark'
    )
    mark_value = models.PositiveSmallIntegerField(
        'Mark',
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    author = models.ForeignKey(
        get_user_model(),
        verbose_name='Author',
        on_delete=models.CASCADE,
        related_name='added_marks'
    )
    updated_at = models.DateTimeField('Updated time', auto_now=True)

    class Meta:
        verbose_name = 'Mark'
        verbose_name_plural = 'Marks'

    def __str__(self):
        return f'{self.author}: {self.mark_value} ({self.updated_at})'


class Message(models.Model):
    '''Message model.
    Teacher of course can add message to the mark of student's task.
    Student can add message to his mark.
    '''

    mark = models.ForeignKey(
        Mark,
        verbose_name='Mark',
        on_delete=models.CASCADE,
        related_name='messages'
    )
    text = models.TextField(max_length=2048)

    author = models.ForeignKey(
        get_user_model(),
        verbose_name='Author',
        on_delete=models.CASCADE,
        related_name='messages'
    )
    parent = models.ForeignKey(
        'self',
        verbose_name='parent',
        on_delete=models.SET_NULL,
        null=True,
        related_name='children'
    )
    created_at = models.DateTimeField('Creation time', auto_now_add=True)

    class Meta:
        ordering = ['created_at']
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'

    def __str__(self):
        return '{}: {}'.format(self.author, self.text[:64])
