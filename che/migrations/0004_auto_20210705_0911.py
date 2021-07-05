# Generated by Django 3.0 on 2021-07-05 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('che', '0003_abono_factura_cheque_equivocado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cheque',
            name='cantidad',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=9),
        ),
    ]
