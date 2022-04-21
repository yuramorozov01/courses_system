from django.db import models
from django.utils.translation import gettext_lazy as _


class CardFundingTypeChoices(models.TextChoices):
    CREDIT = 'credit', _('Credit')
    DEBIT = 'debit', _('Debit')
    PREPAID = 'prepaid', _('Prepaid')
    UNKNOWN = 'unknown', _('Unknown')


class PaymentStatusChoices(models.TextChoices):
    REQUIRES_PAYMENT_METHOD = 'requires_payment_method', _('Requires payment method')
    REQUIRES_CONFIRMATION = 'requires_confirmation', _('Requires confirmation')
    REQUIRES_ACTION = 'requires_action', _('Requires action')
    PROCESSING = 'processing', _('Processing')
    REQUIRES_CAPTURE = 'requires_capture', _('Requires capture')
    CANCELED = 'canceled', _('Canceled')
    SUCCEEDED = 'succeeded', _('Succeeded')
