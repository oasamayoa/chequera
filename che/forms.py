from django import forms
from .models import Cheque, Deposito
from django.contrib.admin import widgets


class ChequeForm(forms.ModelForm):
    class Meta:
        model=Cheque

        fields = [
        'no_cheque',
        'fecha_creado',
        'fecha_pagar',
        'cantidad',
        'no_fac',
        'cuenta',
        'proveedor',
        'imagen',
        'estado',
        'status'
        ]

        exclude = ['um','fm','uc', 'estado_che']

        labels = {
         'no_cheque':"No. Cheque",
         'fecha_creado':"Fecha creado",
         'fecha_pagar':"Fecha a Pagar",
         'cantidad':"Cantidad",
         'no_fac':"No. Factura",
         'cuenta':"Cuentas",
         'proveedor':"Pagar a:",
         'imagen': "Imagen del Cheque",
         'status': "Marcar Cheque Rechezado",
         }
        widgets = {
            'no_cheque': forms.TextInput(attrs={'class':'form-control'}),
            'fecha_pagar': widgets.AdminDateWidget(),
            'cantidad': forms.TextInput(attrs={'class':'form-control'}),
            'no_fac': forms.TextInput(attrs={'class':'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class':'form-control'
            })

        self.fields['cuenta'].empty_label = "Selecione cuenta"
        self.fields['proveedor'].empty_label = "Pagar a:"

class DepositoForm(forms.ModelForm):
    class Meta:
        model=Deposito

        fields = [
        'no_depo',
        'cantidad',
        'fecha_creado',
        'cheque',
        'imagen_dep',

        ]

        exclude = ['um','fm','uc', 'proveedor', 'cuenta', 'no_cheque']

        labels = {
         'no_depo':"No. Deposito",
         'cantidad':"Cantidad",
         'fecha_creado':"Fecha del Deposito",
         'cheque':"No. Cheque",
         'imagen_dep':"Img. Depo.",

         }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class':'form-control'
            })
