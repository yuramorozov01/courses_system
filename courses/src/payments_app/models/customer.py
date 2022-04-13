from django.contrib.auth import get_user_model
from django.db import models


class Customer(models.Model):
    user = models.OneToOneField(
        get_user_model(),
        verbose_name='User',
        on_delete=models.SET_NULL,
        related_name='customer',
        null=True
    )
    stripe_id = models.CharField('Stripe customer ID', max_length=254, editable=False, unique=True)

    class Meta:
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'

    def __str__(self):
        return f'{self.user}: {self.stripe_id}'
