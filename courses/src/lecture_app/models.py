from base_app.utils import get_unique_filename
from django.contrib.auth import get_user_model
from django.db import models


class Lecture(models.Model):
    '''Lecture model.
    Teacher of course can add lecture to the course.
    '''

    course = models.ForeignKey(
        'course_app.Course',
        verbose_name='Course',
        on_delete=models.CASCADE,
        related_name='lectures'
    )
    title = models.CharField('Title', max_length=128)
    text = models.TextField('Text', max_length=8192)
    author = models.ForeignKey(
        get_user_model(),
        verbose_name='Author',
        on_delete=models.CASCADE,
        related_name='own_lectures'
    )
    created_at = models.DateTimeField('Creation time', auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Lecture'
        verbose_name_plural = 'Lectures'

    def __str__(self):
        return self.title


class LectureFile(models.Model):
    '''Lecture file model.
    Attached files to a lecture.
    '''

    lecture = models.ForeignKey(
        Lecture,
        verbose_name='Lecture',
        on_delete=models.CASCADE,
        related_name='files'
    )
    file = models.FileField('File', upload_to=get_unique_filename)
    author = models.ForeignKey(
        get_user_model(),
        verbose_name='Author',
        on_delete=models.CASCADE,
        related_name='own_lecture_files'
    )

    class Meta:
        verbose_name = 'Lecture file'
        verbose_name_plural = 'Lecture files'

    def __str__(self):
        return f'{self.author} | {self.file.path}'
