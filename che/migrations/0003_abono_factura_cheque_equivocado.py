# Generated by Django 3.0 on 2021-03-24 15:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('che', '0002_auto_20210322_0817'),
    ]

    operations = [
        migrations.AddField(
            model_name='abono_factura',
            name='cheque_equivocado',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='che_abono_factura_eq', to='che.Cheque'),
        ),
    ]
