# Generated by Django 5.0.6 on 2024-06-17 08:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("analytics", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="product_id",
            field=models.BigIntegerField(unique=True),
        ),
    ]