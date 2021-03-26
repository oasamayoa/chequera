# Generated by Django 3.0 on 2021-03-26 18:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Empleado',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.BooleanField(default=True)),
                ('fc', models.DateTimeField(auto_now_add=True)),
                ('fm', models.DateTimeField(auto_now_add=True)),
                ('um', models.IntegerField(blank=True, null=True)),
                ('nombre', models.CharField(max_length=50)),
                ('apellido', models.CharField(max_length=50)),
                ('dpi', models.CharField(max_length=25)),
                ('nit', models.CharField(blank=True, max_length=15, null=True)),
                ('no_iggs', models.CharField(blank=True, max_length=20, null=True)),
                ('no_casa', models.IntegerField(blank=True, default=0, null=True)),
                ('no_celular', models.IntegerField(default=0)),
                ('direccion', models.TextField()),
                ('fecha_nacimiento', models.DateField()),
                ('inicio_laboral', models.DateField()),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('imagen_contrato', models.ImageField(blank=True, null=True, upload_to='empleado/')),
                ('imagen_foto', models.ImageField(blank=True, null=True, upload_to='empleado/')),
                ('estado_empleado', models.BooleanField(default=None)),
                ('uc', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Empleado',
                'verbose_name_plural': 'Empleados',
                'db_table': 'Empleado',
            },
        ),
    ]
