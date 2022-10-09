from django.db import models
from enum import IntEnum


class State(IntEnum):
    SUCCESS = 1
    ERROR = 2


class QueryLog(models.Model):
    query = models.TextField()
    created = models.DateTimeField(auto_now=True)
    state = models.SmallIntegerField()

    class Meta:
        permissions = [('can_execute_query', 'Can Execute Query')]