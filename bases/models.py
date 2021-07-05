from django.db import models

from django.contrib.auth.models import User
from django.db.models.fields import CharField

# fc = fecha de creacion, fm = fecha modifichado, uc = usuario, um = usuario modifica


class ClaseModelo(models.Model):
    estado = models.BooleanField(default=True)
    fc = models.DateTimeField(auto_now_add=True)
    fm = models.DateTimeField(auto_now_add=True)
    uc = models.ForeignKey(User, on_delete=models.CASCADE)
    um = models.IntegerField(blank=True, null=True)

    class Meta:
        abstract = True
