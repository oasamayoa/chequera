from django.db import models
from bases.models import ClaseModelo


class Banco(ClaseModelo):
    nombre = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return "{}".format(self.nombre)

    def save(self):
        self.nombre = self.nombre.upper()
        super(Banco, self).save()

    class Meta:
        verbose_name_plural = "Bancos"


class Cuenta(ClaseModelo):
    banco = models.ForeignKey(Banco, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100, help_text="Nombre de la Cuenta")

    def __str__(self):
        return "{}:{}".format(self.banco, self.nombre)

    def save(self):
        self.nombre = self.nombre.upper()
        super(Cuenta, self).save()

    class Meta:
        verbose_name_plural = "Cuentas"
        unique_together = ("banco", "nombre")


class Provedor(ClaseModelo):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return "{}".format(self.nombre)

    def save(self):
        self.nombre = self.nombre.upper()
        super(Provedor, self).save()

    class Meta:
        verbose_name_plural = "Provedores"
