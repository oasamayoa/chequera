from django.db import models
from bases.models import ClaseModelo
from registro.models import Cuenta, Provedor

class Cheque(ClaseModelo):

    no_cheque = models.CharField(max_length=200)
    cantidad = models.FloatField(default=0)
    fecha_pagar = models.DateField()
    fecha_creado = models.DateField()
    no_fac = models.CharField(max_length=20)
    imagen = models.ImageField(upload_to='cheques/')

    cuenta = models.ForeignKey(Cuenta, on_delete=models.CASCADE)
    proveedor = models.ForeignKey(Provedor, on_delete=models.CASCADE)


    def __str__(self):
        return '{}'.format(self.no_cheque)


    class Meta:
        verbose_name_plural = "Cheques"
