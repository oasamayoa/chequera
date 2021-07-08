from django import forms
from django.forms import widgets

from .models import Banco, Cuenta, Provedor


class BancoForm(forms.ModelForm):
    class Meta:
        model = Banco
        fields = "__all__"
        labels = {"nombre": ""}
        exclude = ["uc", "um", "estado"]

        widgets = {
            "nombre": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Nombre del banco",
                    "autocomplete": "off",
                }
            ),
        }

    def clean(self):
        try:
            sc = Banco.objects.get(nombre=self.cleaned_data["nombre"].upper())

            if not self.instance.pk:
                print("Registro ya existe")
                raise forms.ValidationError("Registro Ya Existe")
            elif self.instance.pk != sc.pk:
                print("Cambio no permitido")
                raise forms.ValidationError("Cambio No Permitido")
        except Banco.DoesNotExist:
            pass
        return self.cleaned_data


class CuentaForm(forms.ModelForm):

    banco = forms.ModelChoiceField(
        queryset=Banco.objects.filter(estado=True).order_by("nombre"),
        widget=forms.Select(
            attrs={
                "class": "form-control select2",
                "style": "width: 100%",
                "autocomplete": "off",
            }
        ),
    )

    class Meta:
        model = Cuenta
        fields = "__all__"
        exclude = ["estado", "fc", "uc"]

        widgets = {
            "nombre": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ingresar",
                    "autocomplete": "off",
                    "style": "width: 100%",
                }
            ),
        }


class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Provedor
        fields = ["nombre"]
        labels = {"nombre": ""}
        exclude = ["estado"]
        widget = {"nombre": forms.TextInput()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update(
                {
                    "class": "form-control",
                    "placeholder": "Proveedor",
                    "style": "width: 100%",
                    "autocomplete": "off",
                }
            )

    def clean(self):
        try:
            sc = Provedor.objects.get(nombre=self.cleaned_data["nombre"].upper())

            if not self.instance.pk:
                print("Registro ya existe")
                raise forms.ValidationError("Registro Ya Existe")
            elif self.instance.pk != sc.pk:
                print("Cambio no permitido")
                raise forms.ValidationError("Cambio No Permitido")
        except Provedor.DoesNotExist:
            pass
        return self.cleaned_data
