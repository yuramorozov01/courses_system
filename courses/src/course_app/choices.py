from django.db import models
from django.utils.translation import gettext_lazy as _


class StatusChoices(models.TextChoices):
    OPEN = 'OP', _('Open')
    CLOSED = 'CL', _('Closed')
