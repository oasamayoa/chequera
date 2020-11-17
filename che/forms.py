from django import forms
from .models import Cheque, Deposito
from registro.models import Cuenta, Provedor
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

        exclude = ['um','fm','uc', 'estado']

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
            'no_fac': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'style': 'width: 100%',
                    'autocomplete': 'off'
                }
            ),
            'cantidad': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'style': 'width: 100%',
                    'autocomplete': 'off'
                }
            ),
            'no_cheque': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'style': 'width: 100%',
                    'autocomplete': 'off'
                }
            ),
            'fecha_pagar': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'style': 'width: 100%',
                    'autocomplete': 'off'
                }
            ),
            'fecha_creado': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'style': 'width: 100%',
                    'autocomplete': 'off'
                }
            ),
            'cuenta': forms.Select(
                attrs={
                    'class': 'form-control select2',
                    'style': 'width: 100%',
                    'autocomplete': 'off'
                }
            ),
            'proveedor': forms.Select(
                attrs={
                    'class': 'form-control select2',
                    'style': 'width: 100%',
                    'autocomplete': 'off'
                }
            ),
        }


    cuenta = forms.ModelChoiceField(queryset=Cuenta.objects.all(), widget=forms.Select(attrs={
        'class': 'form-control select2',
        'style': 'width: 100%'
    }))
    proveedor = forms.ModelChoiceField(queryset=Provedor.objects.all(), widget=forms.Select(attrs={
        'class': 'form-control select2',
        'style': 'width: 100%'
    }))

        # self.fields['cuenta'].empty_label = "Selecione cuenta"
        # self.fields['proveedor'].empty_label = "Pagar a:"

class DepositoForm(forms.ModelForm):

    cheque = forms.ModelChoiceField(queryset=Cheque.objects.filter(estado_che=False), widget=forms.Select(attrs={
    'class': 'form-control select2',
    'style': 'width: 100%'
    }))



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

        widgets = {

            'no_depo': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'style': 'width: 100%',
                    'autocomplete': 'off'
                }
            ),
            'cantidad': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'style': 'width: 100%',
                    'autocomplete': 'off'
                }
            ),
            'fecha_creado': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'style': 'width: 100%',
                    'autocomplete': 'off'
                }
            ),


        }
