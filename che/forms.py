from django import forms
from .models import Cheque, Deposito, Fisico_Entregado, Cheque_rechazado, Factura, Abono_Factura
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
        'cuenta',
        'proveedor',
        'imagen',
        'estado',
        'status',
        'estado_che',
        'id_fac',
        ]

        exclude = ['um','fm','uc', 'estado', 'no_fac']

        labels = {
         'no_cheque':"No. Cheque",
         'fecha_creado':"Fecha creado",
         'fecha_pagar':"Fecha a Pagar",
         'cantidad':"Cantidad",
         'id_fac':"No. Factura",
         'cuenta':"Cuentas",
         'proveedor':"Pagar a:",
         'imagen': "Imagen del Cheque",
         'status': "Marcar Cheque Rechezado",
         'estado_che': 'Estado'

        }
        widgets = {
            'id_fac': forms.Select(
                attrs={
                    'class': 'form-control select2',
                    'style': 'width: 100%',
                    'autocomplete': 'off'
                }
            ),
            # 'estado_che': forms.TextInput(
            #     attrs={
            #         'class': 'form-control',
            #     }
            # ),
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

    id_fac = forms.ModelChoiceField(queryset=Factura.objects.all(), widget=forms.Select(attrs={
        'class': 'form-control select2',
        'style': 'width: 100%'
    }))

    cuenta = forms.ModelChoiceField(queryset=Cuenta.objects.all(), widget=forms.Select(attrs={
        'class': 'form-control select2',
        'style': 'width: 100%'
    }))
    proveedor = forms.ModelChoiceField(queryset=Provedor.objects.all(), widget=forms.Select(attrs={
        'class': 'form-control select2',
        'style': 'width: 100%'
    }))

    def clean_no_cheque(self):
        no_cheque = self.cleaned_data.get('no_cheque')

        if Cheque.objects.filter(no_cheque=no_cheque).exists():
            raise forms.ValidationError('El No. de cheque ya existe')
        return no_cheque

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

class CheEntregadoForm(forms.ModelForm):

    cheque = forms.ModelChoiceField(queryset=Cheque.objects.filter(estado_che=False), widget=forms.Select(attrs={
    'class': 'form-control select2',
    'style': 'width: 100%'
    }))



    class Meta:
        model=Fisico_Entregado

        fields = ['nombre', 'cheque']

        exclude = ['um','fm','uc','fecha_creado' ]

        labels = {
         'nombre':"Nombre del cliente",
         'cheque':"Cheque ",

         }

        widgets = {

            'nombre': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'style': 'width: 100%',
                    'autocomplete': 'off'
                }
            ),

        }

class CheRechazadoForm(forms.ModelForm):

    cheque_re = forms.ModelChoiceField(queryset=Cheque.objects.all(), widget=forms.Select(attrs={
    'class': 'form-control select2',
    'style': 'width: 100%'
    }))

    cheque_nu = forms.ModelChoiceField(queryset=Cheque.objects.filter(status=None), widget=forms.Select(attrs={
    'class': 'form-control select2',
    'style': 'width: 100%'
    }))



    class Meta:
        model=Cheque_rechazado

        fields = ['cheque_re', 'cheque_nu', 'observacion']

        exclude = ['um','fm','uc' ]

        labels = {
         'cheque_re':"Cheque rechazado",
         'cheque_nu':"Cheque Nuevo ",
         'observacion': "Observaciones"

         }

        widgets = {

            'observacion': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'style': 'width: 100%',
                    'autocomplete': 'off'
                }
            ),

        }



class FacturaForm(forms.ModelForm):

    proveedor = forms.ModelChoiceField(queryset=Provedor.objects.all(), widget=forms.Select(attrs={
    'class': 'form-control select2',
    'style': 'width: 100%'
    }))


    class Meta:
        model=Factura

        fields = ['no_fac', 'fecha_pagar', 'proveedor', 'total_fac', 'total_fac1']

        exclude = ['um','fm','uc', 'imagen_fac' ]

        labels = {
         'no_fac':"No. Factura",
         'fecha_pagar':"Fecha a pagar factura",
         'proveedor': "Pagar a",
         'total_fac': "Total factura",
         'total_fac1': "Confirmacion de Total"

         }

        widgets = {

            'no_fac': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'style': 'width: 100%',
                    'autocomplete': 'off'
                }
            ),
            'fecha_pagar': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'autocomplete': 'off'
                }
            ),
            'total_fac': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'autocomplete': 'off'
                }
            ),
            'total_fac1': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'autocomplete': 'off'
                }
            ),

        }

    def clean_total_fac1(self):
        total_fac = self.cleaned_data.get('total_fac')
        total_fac1 = self.cleaned_data.get('total_fac1')
        print(total_fac)
        print(total_fac1)
        if total_fac != total_fac1:
            raise forms.ValidationError('No coincide')
        return total_fac1


class AbonoForm(forms.ModelForm):

    id_factura = forms.ModelChoiceField(queryset=Factura.objects.all(), widget=forms.Select(attrs={
    'class': 'form-control select2',
    'style': 'width: 100%'
    }))

    id_cheque = forms.ModelChoiceField(queryset=Cheque.objects.all(), widget=forms.Select(attrs={
    'class': 'form-control select2',
    'style': 'width: 100%'
    }))

    class Meta:
        model = Abono_Factura

        fields = ['id_factura', 'id_cheque']

        exclude = ['um','fm','uc', 'total', 'estado_abono']
