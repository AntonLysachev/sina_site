from django.db import models
from sina_site.customers.models import Customer


class Review(models.Model):
    review = models.TextField(blank=True, null=True)
    grade = models.IntegerField()
    customer = models.ForeignKey(Customer, models.DO_NOTHING)
    type = models.CharField(max_length=10)
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'reviews'
