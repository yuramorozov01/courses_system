from django.contrib.auth import get_user_model
from django.db import models


class Customer(models.Model):
    user = models.OneToOneField(
        get_user_model(),
        verbose_name='User',
        on_delete=models.CASCADE,
        related_name='customer'
    )
    stripe_id = models.CharField('Stripe customer ID', max_length=256, editable=False, unique=True)


# class Card(models.Model):
#     user = models.ForeignKey(
#         get_user_model(),
#         verbose_name='User',
#         on_delete=models.CASCADE,
#         related_name='cards'
#     )
#
#
#     class Meta:
#         verbose_name = 'Card'
#         verbose_name_plural = 'Cards'
#
#     # def __str__(self):
#     #     return self.title
#
#
# class Payment(models.Model):
#     pass
