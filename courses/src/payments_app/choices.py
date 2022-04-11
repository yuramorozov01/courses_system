from django.db import models
from django.utils.translation import gettext_lazy as _


class CardFundingTypeChoices(models.TextChoices):
    CREDIT = 'credit', _('Credit')
    DEBIT = 'debit', _('Debit')
    PREPAID = 'prepaid', _('Prepaid')
    UNKNOWN = 'unknown', _('Unknown')
