from django.db import models
from sina_site.customers.models import Customer


class Product(models.Model):
    product_id = models.BigIntegerField(unique=True)
    type = models.BigIntegerField()
    product_sum = models.FloatField()
    payed_sum = models.FloatField()


class Transaction(models.Model):
    transaction_id = models.BigIntegerField(unique=True)
    client_id = models.BigIntegerField()
    date_close = models.DateTimeField()
    product_id = models.ManyToManyField(Product)
    customer_id = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
