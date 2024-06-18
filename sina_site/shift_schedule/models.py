from django.db import models

class Shift(models.Model):
    name = models.CharField(max_length=200)
    monday = models.CharField(max_length=200, blank=True)
    tuesday = models.CharField(max_length=200, blank=True)
    wednesday = models.CharField(max_length=200, blank=True)
    thursday = models.CharField(max_length=200, blank=True)
    friday = models.CharField(max_length=200, blank=True)
    saturday = models.CharField(max_length=200, blank=True)
    sunday = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.name
