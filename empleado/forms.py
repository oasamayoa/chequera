from django import forms
from empleado.views import Farmacia, Empleado

class FarmaciaForm(forms.ModelForm):

    class Meta:
        # error_css_class = 'has-error' # si trabajas con bootstrap
        model = Farmacia

        fields = ['nombre']

        exclude= ['um','fm','uc', 'estado_farm']

        widgets = {
            'nombre': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'style': 'width: 100%',
                    'autocomplete': 'off'
                }
            ),
        }
