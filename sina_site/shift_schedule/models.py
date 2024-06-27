from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Shift(models.Model):
    worker = models.ForeignKey(User, on_delete=models.SET_NULL, default=None, null=True)
    date = models.DateField(default=timezone.now)
    shift = models.IntegerField(default=0)

    class Meta:
        unique_together = ('date', 'shift')