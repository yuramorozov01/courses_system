import arrow
from celery import Task as CeleryTask
from course_app.choices import StatusChoices as CourseStatusChoices
from course_app.models import Course
from courses.celery import app
from django.db.transaction import atomic
from payments_app.choices import PaymentStatusChoices
from libs.payments import PaymentService


class CaptureStartedCoursesTask(CeleryTask):
    @atomic
    def run(self, *args, **kwargs):
        today = arrow.now().date()
        courses = Course.objects.filter(
            starts_at=today,
            payments__payment__status=PaymentStatusChoices.REQUIRES_CAPTURE
        )
        result = []
        for course in courses:
            payments_courses = course.payments.all()
            course_result = {
                'course_id': course.id,
                'payments': [],
            }
            for payment_course in payments_courses:
                payment_service = PaymentService(payment_course.user)
                payment = payment_service.capture_money(payment_course.payment, course.price)
                course_result['payments'].append(payment.id)

            result.append(course_result)
        return result


app.register_task(CaptureStartedCoursesTask)
