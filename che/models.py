from django.db import models
from bases.models import ClaseModelo
from registro.models import Cuenta, Provedor
from django.utils import timezone
from datetime import date


class Cheque(ClaseModelo):

    no_cheque = models.CharField(max_length=200)
    estado_che = models.BooleanField(default=False)
    cantidad = models.FloatField(default=0)
    fecha_pagar = models.DateField(blank=True)
    fecha_creado = models.DateField('feche creado',  auto_now = False, default = date.today)
    no_fac = models.CharField(max_length=20)
    imagen = models.ImageField(upload_to='cheques/' , null=True, blank=True)

    cuenta = models.ForeignKey(Cuenta, on_delete=models.CASCADE)
    proveedor = models.ForeignKey(Provedor, on_delete=models.CASCADE)

    LOAN_STATUS = (
        ('R', 'R'),
        ('E', 'E'),
    )
    status = models.CharField(max_length=1, choices=LOAN_STATUS, null=True, blank=True)

    def __str__(self):
        return '{}'.format(self.no_cheque)


    class Meta:
        verbose_name_plural = "Cheques"

class Deposito(ClaseModelo):
    no_depo = models.CharField(max_length=50)
    cantidad = models.FloatField(default=0)
    fecha_creado = models.DateField('feche creado',  auto_now = False, default = date.today)
    cheque = models.ForeignKey(Cheque, on_delete=models.CASCADE)
    imagen_dep = models.ImageField(upload_to='deposito/' , null=True, blank=True)

    def __str__(self):
        return '{}'.format(self.no_depo)


    class Meta:
        verbose_name_plural = "Depositos"

class Fisico_Entregado(ClaseModelo):
    nombre = models.CharField('Nombre al que se le entrego', max_length=50)
    fecha_creado = models.DateField(auto_now_add=True)
    cheque = models.ForeignKey(Cheque, on_delete=models.CASCADE)


    def __str__(self):
        return '{}'.format(self.nombre)


    class Meta:
        verbose_name = 'Cheque entregado'
        verbose_name_plural = 'Cheques entregados'
        db_table = 'Che_Fisico'
