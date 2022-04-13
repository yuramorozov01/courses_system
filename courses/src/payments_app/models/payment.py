from django.contrib.auth import get_user_model
from django.db import models
from payments_app.choices import PaymentStatusChoices


class Payment(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        verbose_name='User',
        on_delete=models.SET_NULL,
        related_name='payments',
        null=True
    )
    course = models.ForeignKey(
        'course_app.Course',
        verbose_name='Course',
        on_delete=models.SET_NULL,
        related_name='payments',
        null=True
    )
    payment_intent_id = models.CharField('Payment intent ID', max_length=254, editable=False, unique=True)
    payment_method_id = models.CharField('Payment method ID', max_length=254, editable=False)
    amount = models.PositiveIntegerField('Amount')
    currency = models.CharField('Currency', max_length=3)
    customer = models.ForeignKey(
        'payments_app.Customer',
        verbose_name='Customer',
        on_delete=models.SET_NULL,
        related_name='payments',
        null=True
    )
    status = models.CharField(
        'Status',
        choices=PaymentStatusChoices.choices,
        max_length=32
    )
    created = models.DateTimeField('Created at')

    class Meta:
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'

    def __str__(self):
        return f'{self.course}: {self.amount} - {self.created} - {self.get_status_display()} ({self.user})'
