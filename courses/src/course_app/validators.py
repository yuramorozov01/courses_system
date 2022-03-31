import arrow

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_date(value):
    if value < arrow.now().date():
        raise ValidationError(
            _('%(value)s is not correct! Specify date that\'s not in the past!'),
            params={'value': value},
        )
