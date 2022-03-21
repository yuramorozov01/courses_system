from celery import Task as CeleryTask
from courses.celery import app
from django.db.models import Count
from course_app.models import Course


class CalcAmountOfStudentsInCourseTask(CeleryTask):
    def run(self, *args, **kwargs):
        courses_with_amount_of_students = Course.objects.annotate(amount_of_students=Count('students'))
        return list(courses_with_amount_of_students.values())


app.register_task(CalcAmountOfStudentsInCourseTask)
