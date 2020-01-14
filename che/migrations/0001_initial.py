# Generated by Django 3.0 on 2020-01-14 02:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('registro', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cheque',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.BooleanField(default=True)),
                ('fc', models.DateTimeField(auto_now_add=True)),
                ('fm', models.DateTimeField(auto_now_add=True)),
                ('um', models.IntegerField(blank=True, null=True)),
                ('no_cheque', models.CharField(max_length=200)),
                ('cantidad', models.FloatField(default=0)),
                ('fecha_pagar', models.DateField()),
                ('fecha_creado', models.DateField()),
                ('no_fac', models.CharField(max_length=20)),
                ('imagen', models.ImageField(upload_to='cheques/')),
                ('cuenta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='registro.Cuenta')),
                ('proveedor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='registro.Provedor')),
                ('uc', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Cheques',
            },
        ),
    ]
