# Generated by Django 3.0 on 2020-01-18 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('che', '0003_cheque_estado_che'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cheque',
            name='estado_che',
            field=models.BooleanField(default=False),
        ),
    ]
