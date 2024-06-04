from django.db import models

class Customer(models.Model):
    phone = models.CharField(unique=True)
    chat_id = models.BigIntegerField(unique=True)
    poster_id = models.BigIntegerField(unique=True)
    firstname = models.CharField(max_length=50, blank=True, null=True)
    lastname = models.CharField(max_length=50, blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    group_name = models.CharField(max_length=10)
    is_active = models.BooleanField()
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'customers'
