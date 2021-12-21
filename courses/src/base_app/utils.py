import os
import uuid

from django.conf import settings


def get_unique_filename(instance, filename):
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid.uuid4(), ext)
    return 'user_{0}/{1}'.format(instance.author.id, filename)
