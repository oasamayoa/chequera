from django.db import models
from bases.models import ClaseModelo
from registro.models import Cuenta, Provedor
from django.utils import timezone
from datetime import date, datetime
from chequera.settings import MEDIA_URL, STATIC_URL
from django.forms import model_to_dict


class Factura(ClaseModelo):
    no_fac = models.CharField("Factura", unique=True, max_length=25)
    total_fac = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    estado_fac = models.NullBooleanField(default=0)
    fecha_pagar = models.DateField(blank=True)
    imagen_fac = models.ImageField(upload_to="factura/", null=True, blank=True)
    total_fac1 = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    proveedor = models.ForeignKey(Provedor, on_delete=models.CASCADE)

    def __str__(self):
        return "No. {} -- Total {}".format(self.no_fac, self.total_fac)

    def get_factura_name(self):
        return "No.{} -- Valor {}".format(self.no_fac, self.total_fac)

    @property
    def abonos_facturas(self):
        return self.abono_factura_set.all()

    # def save(self):
    #     self.total_fac1 = self.total_fac
    #     super(Factura, self).save()

    def toJSON(self):
        item = model_to_dict(
            self, exclude=["proveedor", "estado", "fc", "fm", "uc", "um", "imagen_fac"]
        )
        item["total_fac1"] = format(self.total_fac1, ".2f")
        item["total_fac"] = format(self.total_fac, ".2f")
        item["get_factura_name"] = self.get_factura_name()
        item["no_fac"] = self.no_fac
        return item

    class Meta:
        verbose_name = "Factura"
        verbose_name_plural = "Facturas"
        db_table = "Factura"


class Cheque(ClaseModelo):

    no_cheque = models.CharField(max_length=200)
    estado_che = models.BooleanField(default=False)
    cantidad = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    fecha_pagar = models.DateField(blank=True)
    fecha_creado = models.DateField("feche creado", auto_now=False, default=date.today)
    no_fac = models.CharField(max_length=20)
    imagen = models.ImageField(upload_to="cheques/", null=True, blank=True)

    cuenta = models.ForeignKey(Cuenta, on_delete=models.CASCADE)
    proveedor = models.ForeignKey(Provedor, on_delete=models.CASCADE)
    id_fac = models.ForeignKey(Factura, on_delete=models.CASCADE)

    LOAN_STATUS = (("E", "E"),)
    status = models.CharField(max_length=1, choices=LOAN_STATUS, null=True, blank=True)

    def __str__(self):
        return "No. {} -- Total {}".format(self.no_cheque, self.cantidad)

    def get_img(self):
        if self.imagen:
            return "{}{}".format(MEDIA_URL, self.imagen)
        return "{}{}".format(STATIC_URL, "base/img/blanco.png")

    @property
    def cheques_rechazados(self):
        return self.cheque_rechazado_set.all()

    class Meta:
        verbose_name_plural = "Cheques"

    def natural_key(self):
        return self.no_cheque


class Deposito(ClaseModelo):
    no_depo = models.CharField(max_length=50)
    cantidad = models.FloatField(default=0)
    fecha_creado = models.DateField("feche creado", auto_now=False, default=date.today)
    cheque = models.ForeignKey(Cheque, on_delete=models.CASCADE)
    imagen_dep = models.ImageField(upload_to="deposito/", null=True, blank=True)

    def __str__(self):
        return "{}".format(self.no_depo)

    def get_img_depo(self):
        if self.imagen_dep:
            return "{}{}".format(MEDIA_URL, self.imagen_dep)
        return "{}{}".format(STATIC_URL, "base/img/blanco.png")

    class Meta:
        verbose_name_plural = "Depositos"


class Fisico_Entregado(ClaseModelo):
    nombre = models.CharField("Nombre al que se le entrego", max_length=50)
    fecha_creado = models.DateField(auto_now_add=True)
    cheque = models.ForeignKey(Cheque, on_delete=models.CASCADE)

    def __str__(self):
        return "{}".format(self.nombre)

    class Meta:
        verbose_name = "Cheque entregado"
        verbose_name_plural = "Cheques entregados"
        db_table = "Che_Fisico"


class Cheque_rechazado(ClaseModelo):
    cheque_re = models.ForeignKey(Cheque, on_delete=models.CASCADE)
    cheque_nu = models.ForeignKey(
        Cheque,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="%(app_label)s_%(class)s_nu",
    )
    observacion = models.CharField("Observacion", max_length=200)
    id_facturas = models.ForeignKey(Factura, on_delete=models.CASCADE)

    def __str__(self):
        return "{}{}".format(self.observacion, self.chere_re)

    class Meta:
        verbose_name = "Cheque rechazado"
        verbose_name_plural = "Cheques rechazados"
        db_table = "Che_rechazado"


class Abono_Factura(ClaseModelo):
    id_factura = models.ForeignKey(Factura, on_delete=models.CASCADE)
    estado_abono = models.BooleanField(default=True)
    id_cheque = models.ForeignKey(
        Cheque, on_delete=models.CASCADE, null=True, blank=True
    )
    cheque_equivocado = models.ForeignKey(
        Cheque,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="%(app_label)s_%(class)s_eq",
    )
    total = models.FloatField(default=0)
    recibo = models.ForeignKey(
        "che.Recibo", on_delete=models.CASCADE, blank=True, null=True
    )

    def __str__(self):
        return "{}".format(self.id_factura)

    # def save(self):
    #     self.total = self.id_factura.total_fac1 - self.id_cheque.cantidad
    #     super(Abono_Factura, self).save()

    class Meta:
        verbose_name = "Abono_Factura"
        verbose_name_plural = "Abonos de Facturas"
        db_table = "Abono_factura"


class Recibo(models.Model):
    no_recibo = models.CharField(max_length=30)
    fecha_creacion = models.DateField(auto_now_add=True, blank=True)
    factura = models.ForeignKey(
        Factura, on_delete=models.CASCADE, null=True, blank=True
    )
    monto = models.DecimalField(default=0.00, decimal_places=2, max_digits=9)

    def __str__(self):
        return "{}".format(self.no_recibo)

    class Meta:
        verbose_name = "Recibo"
        verbose_name_plural = "Recibos"
        db_table = "recibo"
