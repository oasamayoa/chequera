from django import forms
from .models import Cheque

class ChequeForm(forms.ModelForm):
    class Meta:
        model=Cheque
        fields=['no_cheque', 'fecha_pagar','fecha_creado','cantidad','no_fac','cuenta','proveedor','imagen']
        exclude = ['um','fm','uc']
        widget={'no_cheque': forms.TextInput()}


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })


        self.fields['cuenta'].empty_label = "Seleccione Cuenta"
        self.fields['proveedor'].empty_label = "Seleccione Proveedor"
