from django.db import models
from django.conf import settings
from enum import IntEnum


class State(IntEnum):
    SUCCESS = 1
    ERROR = 2


class QueryLog(models.Model):
    query = models.TextField()
    created = models.DateTimeField(auto_now=True)
    state = models.SmallIntegerField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    class Meta:
        permissions = [('can_execute_query', 'Can Execute Query')]