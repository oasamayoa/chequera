# Generated by Django 3.0 on 2021-03-15 16:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('che', '0011_abono_factura'),
    ]

    operations = [
        migrations.AddField(
            model_name='abono_factura',
            name='total',
            field=models.FloatField(default=0),
        ),
    ]