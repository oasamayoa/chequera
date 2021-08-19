from django import forms
from django.db.models import Q
from .models import Cheque, Deposito, Fisico_Entregado, Cheque_rechazado, Factura, Abono_Factura
from registro.models import Cuenta, Provedor
from django.contrib.admin import widgets
from django.db.models import Prefetch


class ChequeForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


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
                    'autocomplete': 'off',
                    'readonly': True
                }
            ),
            'fecha_creado': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'style': 'width: 100%',
                    'autocomplete': 'off',
                    'readonly': True
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
    queryset_id_cheque = Factura.objects.defer("id").filter(Q(total_fac1__gt = 0) | Q(total_fac1__lt = 0)).defer("total_fac").order_by('-id')
    id_fac = forms.ModelChoiceField(queryset=queryset_id_cheque, widget=forms.Select(attrs={
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

class ChequeEditform(forms.ModelForm):
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
                    'autocomplete': 'off',
                    'readonly': True
                }
            ),
            'fecha_creado': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'style': 'width: 100%',
                    'autocomplete': 'off',
                    'readonly': True
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
    # query_id_fac = [factura.id for factura in Factura.objects.filter(Q(total_fac1__gt = 0) | Q(total_fac1__lt = 0)).order_by('-id')]
    queryset_id_cheque = Factura.objects.defer("id").filter(Q(total_fac1__gt = 0) | Q(total_fac1__lt = 0)).defer("total_fac").order_by('-id')
    id_fac = forms.ModelChoiceField(queryset=queryset_id_cheque, widget=forms.Select(attrs={
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


class DepositoForm(forms.ModelForm):

    # query_id_che = [cheque.id for cheque in Cheque.objects.filter(estado_che=False).order_by('-id')]
    queryset_id_cheque = Cheque.objects.defer("id").filter(estado_che=False).defer("estado_che").select_related('id_fac','proveedor','cuenta').order_by('-id')
    cheque = forms.ModelChoiceField(queryset=queryset_id_cheque, widget=forms.Select(attrs={
    'class': 'form-control select2',
    'style': 'width: 100%'
    }))

    # cheque1 = forms.ModelChoiceField(queryset=Cheque.objects.all(), widget=forms.Select(attrs={
    # 'class': 'form-control select2',
    # 'style': 'width: 100%'
    # }))


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
                    'autocomplete': 'off',
                    'readonly': True
                }
            ),
            'cheque': forms.Select(
                attrs={
                    'class': 'form-control select2',
                    'style': 'width: 100%',
                    'autocomplete': 'off'
                }
            ),
        }

class DepositoEditForm(forms.ModelForm):

    # query_id_che = [cheque.id for cheque in Cheque.objects.filter(estado_che=False).order_by('-id')]
    queryset_id_cheque = Cheque.objects.defer("id").filter().defer("estado_che").select_related('id_fac','proveedor','cuenta').order_by('-id')
    cheque = forms.ModelChoiceField(queryset=queryset_id_cheque, widget=forms.Select(attrs={
    'class': 'form-control select2',
    'style': 'width: 100%'
    }))

    # cheque1 = forms.ModelChoiceField(queryset=Cheque.objects.all(), widget=forms.Select(attrs={
    # 'class': 'form-control select2',
    # 'style': 'width: 100%'
    # }))


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
                    'autocomplete': 'off',
                    'readonly': True
                }
            ),
            'cheque': forms.Select(
                attrs={
                    'class': 'form-control select2',
                    'style': 'width: 100%',
                    'autocomplete': 'off'
                }
            ),
        }

class CheEntregadoForm(forms.ModelForm):

    # query_id_che = [cheque.id for cheque in Cheque.objects.filter(estado_che=False).order_by('-id')]
    queryset_id_cheque = Cheque.objects.defer("id").filter(estado_che=False).defer("estado_che").select_related('id_fac','proveedor','cuenta').order_by('-id')
    cheque = forms.ModelChoiceField(queryset=queryset_id_cheque, widget=forms.Select(attrs={
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



    # query_id_che_re = [cheque.id for cheque in Cheque.objects.filter().order_by('-no_cheque')]
    queryset_id_che = Cheque.objects.filter().select_related('id_fac','proveedor','cuenta').order_by('-id')
    cheque_re = forms.ModelChoiceField(queryset=queryset_id_che, widget=forms.Select(attrs={
    'class': 'form-control select2',
    'style': 'width: 100%'
    }))

    # query_id_che_nu = [cheque.id for cheque in Cheque.objects.all().order_by('-id')]
    queryset_id_che = Cheque.objects.filter().select_related('id_fac','proveedor','cuenta').order_by('-id')
    cheque_nu = forms.ModelChoiceField(queryset=queryset_id_che, widget=forms.Select(attrs={
    'class': 'form-control select2',
    'style': 'width: 100%'
    }))

    # query_id_fac = [factura.id for factura in Factura.objects.filter().order_by('-id')]
    queryset_id_fac = Factura.objects.filter().select_related('proveedor').order_by('-id')
    id_facturas = forms.ModelChoiceField(queryset=Factura.objects.all(), widget=forms.Select(attrs={
    'class': 'form-control select2',
    'style': 'width: 100%'
    }))



    class Meta:
        model=Cheque_rechazado

        fields = ['cheque_re', 'cheque_nu', 'observacion', 'id_facturas']

        exclude = ['um','fm','uc' ]

        labels = {
         'cheque_re':"Cheque rechazado",
         'cheque_nu':"Cheque Nuevo ",
         'id_facturas': "No. factura",
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
                    'autocomplete': 'off',
                    'readonly': True
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
        if total_fac != total_fac1:
            raise forms.ValidationError('No coincide')
        return total_fac1

class FacturaFormEdit(forms.ModelForm):

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
                    'autocomplete': 'off',
                    'readonly': True
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


class AbonoForm(forms.ModelForm):

    # query_id_fac = [factura.id for factura in Factura.objects.filter(Q(total_fac1__gt = 0) | Q(total_fac1__lt = 0)).order_by('-id')]
    queryset_id_fa = Factura.objects.defer("id").filter(Q(total_fac1__gt = 0) | Q(total_fac1__lt = 0)).defer("total_fac").select_related('proveedor').order_by('-id')
    id_factura = forms.ModelChoiceField(queryset=queryset_id_fa, widget=forms.Select(attrs={
    'class': 'form-control select2',
    'style': 'width: 100%'
    }))

    # query_id_che = [cheque.id for cheque in Cheque.objects.filter().order_by('-id')]
    queryset_id_che = Cheque.objects.defer("id").filter().select_related('id_fac','proveedor','cuenta').order_by('-id')
    id_cheque = forms.ModelChoiceField(queryset=queryset_id_che, widget=forms.Select(attrs={
    'class': 'form-control select2',
    'style': 'width: 100%'
    }))

    class Meta:
        model = Abono_Factura

        fields = ['id_factura', 'id_cheque']

        exclude = ['um','fm','uc', 'total', 'estado_abono', 'cheque_equivocado']

class AbonoEditForm(forms.ModelForm):

    # query_id_fac = [factura.id for factura in Factura.objects.filter(Q(total_fac1__gt = 0) | Q(total_fac1__lt = 0)).order_by('-id')]
    queryset_id_fa = Factura.objects.defer("id").filter(Q(total_fac1__gt = 0) | Q(total_fac1__lt = 0)).defer("total_fac").select_related('proveedor').order_by('-id')
    id_factura = forms.ModelChoiceField(queryset=queryset_id_fa, widget=forms.Select(attrs={
    'class': 'form-control select2',
    'style': 'width: 100%'
    }))

    # query_id_che = [cheque.id for cheque in Cheque.objects.filter().order_by('-id')]
    queryset_id_che = Cheque.objects.defer("id").filter().select_related('id_fac','proveedor','cuenta').order_by('-id')
    id_cheque = forms.ModelChoiceField(queryset=queryset_id_che, widget=forms.Select(attrs={
    'class': 'form-control select2',
    'style': 'width: 100%'
    }))

    class Meta:
        model = Abono_Factura

        fields = ['id_factura', 'id_cheque']

        exclude = ['um','fm','uc', 'cheque_equivocado','total']

class AbonoEquivocadoForm(forms.ModelForm):

    # query_id_fac = [factura.id for factura in Factura.objects.filter(Q(total_fac1__gt = 0) | Q(total_fac1__lt = 0)).order_by('-id')]
    queryset_id_fa = Factura.objects.defer("id").filter(Q(total_fac1__gt = 0) | Q(total_fac1__lt = 0)).defer("total_fac").select_related('proveedor').order_by('-id')
    id_factura = forms.ModelChoiceField(queryset=queryset_id_fa, widget=forms.Select(attrs={
    'class': 'form-control select2',
    'style': 'width: 100%'
    }))

    # query_id_che = [cheque.id for cheque in Cheque.objects.filter().order_by('-id')]
    queryset_id_che = Cheque.objects.defer("id").filter().select_related('id_fac','proveedor','cuenta').order_by('-id')
    id_cheque = forms.ModelChoiceField(queryset=queryset_id_che, widget=forms.Select(attrs={
    'class': 'form-control select2',
    'style': 'width: 100%'
    }))

    # query_id_che_equi = [cheque.id for cheque in Cheque.objects.filter().order_by('-id')]
    queryset_id_che_e = Cheque.objects.defer("id").filter().select_related('id_fac','proveedor','cuenta').order_by('-id')
    cheque_equivocado = forms.ModelChoiceField(queryset=queryset_id_che_e, widget=forms.Select(attrs={
    'class': 'form-control select2',
    'style': 'width: 100%'
    }))

    class Meta:
        model = Abono_Factura

        fields = ['id_factura', 'id_cheque', 'cheque_equivocado']

        exclude = ['um','fm','uc', 'total', 'estado_abono']
