from course_app.choices import StatusChoices
from course_app.validators import validate_date
from django.contrib.auth import get_user_model
from django.db import models


class Course(models.Model):
    '''Course model.
    User can create his own course.
    Author of course automatically becomes a teacher of this course.
    Teacher of this course can add users as a students to this course.
    Teacher of this course can add users as a teachers to this course.
    Course can be in 2 conditions:
        - Open
        - Closed
    '''

    title = models.CharField('Title', max_length=128)
    created_at = models.DateTimeField('Creation time', auto_now_add=True)
    starts_at = models.DateField(
        'Start date',
        validators=[validate_date]
    )
    ends_at = models.DateField(
        'End date',
        validators=[validate_date]
    )
    author = models.ForeignKey(
        get_user_model(),
        verbose_name='Author',
        on_delete=models.CASCADE,
        related_name='own_courses'
    )
    teachers = models.ManyToManyField(
        get_user_model(),
        blank=True,
        related_name='teaching_courses'
    )
    students = models.ManyToManyField(
        get_user_model(),
        blank=True,
        related_name='attending_courses'
    )
    status = models.TextField(choices=StatusChoices.choices, default=StatusChoices.OPEN)

    class Meta:
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'

    def __str__(self):
        return self.title
