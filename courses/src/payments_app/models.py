from django.contrib.auth import get_user_model
from django.core.validators import (MaxValueValidator, MinLengthValidator,
                                    MinValueValidator)
from django.db import models
from payments_app.choices import CardFundingTypeChoices


class Customer(models.Model):
    user = models.OneToOneField(
        get_user_model(),
        verbose_name='User',
        on_delete=models.CASCADE,
        related_name='customer'
    )
    stripe_id = models.CharField('Stripe customer ID', max_length=254, editable=False, unique=True)

    class Meta:
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'

    def __str__(self):
        return f'{self.user}: {self.stripe_id}'


class Card(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        verbose_name='User',
        on_delete=models.CASCADE,
        related_name='cards'
    )
    pm_id = models.CharField('Payment method ID', max_length=254, editable=False, unique=True)
    name = models.CharField('Billing name', max_length=254)
    brand = models.CharField('Brand', max_length=254)
    country = models.CharField('Country', max_length=32)
    exp_month = models.PositiveSmallIntegerField(
        'Expiration month',
        validators=[MinValueValidator(1), MaxValueValidator(12)]
    )
    exp_year = models.PositiveSmallIntegerField(
        'Expiration year',
        validators=[MinValueValidator(2022)]
    )
    fingerprint = models.CharField('Fingerprint', max_length=254)
    funding = models.CharField(
        'Funding type',
        choices=CardFundingTypeChoices.choices,
        default=CardFundingTypeChoices.UNKNOWN,
        max_length=32
    )
    last4 = models.CharField('Last 4 digits', max_length=4, validators=[MinLengthValidator(4)])
    created = models.DateTimeField('Created at')
    customer = models.ForeignKey(
        Customer,
        verbose_name='Customer',
        on_delete=models.RESTRICT,
        related_name='cards'
    )

    class Meta:
        verbose_name = 'Card'
        verbose_name_plural = 'Cards'

    def __str__(self):
        return f'**** {self.last4} {self.brand} {self.exp_month}/{self.exp_year}'
