# Generated by Django 3.0 on 2020-01-17 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('che', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cheque',
            name='fecha_creado',
            field=models.DateField(verbose_name='feche creado'),
        ),
        migrations.AlterField(
            model_name='cheque',
            name='fecha_pagar',
            field=models.DateField(blank=True),
        ),
        migrations.AlterField(
            model_name='cheque',
            name='imagen',
            field=models.ImageField(blank=True, null=True, upload_to='cheques/'),
        ),
    ]
