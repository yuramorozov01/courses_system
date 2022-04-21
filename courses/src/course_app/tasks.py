import arrow
from celery import Task as CeleryTask
from course_app.choices import StatusChoices as CourseStatusChoices
from course_app.models import Course
from courses.celery import app
from django.db.models import Count
from django.db.transaction import atomic


class CalcAmountOfStudentsInCourseTask(CeleryTask):
    def run(self, *args, **kwargs):
        courses_with_amount_of_students = Course.objects.annotate(amount_of_students=Count('students'))
        return list(courses_with_amount_of_students.values())


class CloseFinishedCoursesTask(CeleryTask):
    @atomic
    def run(self, *args, **kwargs):
        yesterday_date = arrow.now().shift(days=-1).date()
        updated = Course.objects.filter(
            ends_at=yesterday_date,
            status=CourseStatusChoices.OPEN
        ).update(
            status=CourseStatusChoices.CLOSED
        )
        return updated


app.register_task(CalcAmountOfStudentsInCourseTask)
app.register_task(CloseFinishedCoursesTask)
