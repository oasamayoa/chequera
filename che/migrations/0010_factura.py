# Generated by Django 3.0 on 2021-02-08 15:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('registro', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('che', '0009_cheque_rechazado'),
    ]

    operations = [
        migrations.CreateModel(
            name='Factura',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.BooleanField(default=True)),
                ('fc', models.DateTimeField(auto_now_add=True)),
                ('fm', models.DateTimeField(auto_now_add=True)),
                ('um', models.IntegerField(blank=True, null=True)),
                ('no_fac', models.CharField(max_length=25, unique=True, verbose_name='Factura')),
                ('total_fac', models.FloatField(default=0)),
                ('estado_fac', models.NullBooleanField(default=0)),
                ('fecha_pagar', models.DateField(blank=True)),
                ('imagen_fac', models.ImageField(blank=True, null=True, upload_to='factura/')),
                ('proveedor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='registro.Provedor')),
                ('uc', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Factura',
                'verbose_name_plural': 'Facturas',
                'db_table': 'Factura',
            },
        ),
    ]
