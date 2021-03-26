from django.db import models
from bases.models import ClaseModelo

class Empleado(ClaseModelo):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    dpi = models.CharField(max_length=25)
    nit = models.CharField(max_length=15, null=True, blank=True)
    no_iggs = models.CharField(max_length=20, null=True, blank=True)
    no_casa = models.IntegerField(default=0, null=True, blank=True)
    no_celular = models.IntegerField(default=0)
    direccion = models.TextField()
    fecha_nacimiento = models.DateField()
    inicio_laboral = models.DateField()
    email = models.EmailField(null = True, blank= True)
    imagen_contrato = models.ImageField(upload_to='empleado/' , null=True, blank=True)
    imagen_foto = models.ImageField(upload_to='empleado/' , null=True, blank=True)
    estado_empleado = models.BooleanField(default=None)

    def __str__(self):
        return '{}{}'.format(self.nombre, self.apellido)

    class Meta:
        verbose_name = 'Empleado'
        verbose_name_plural = 'Empleados'
        db_table = 'Empleado'
