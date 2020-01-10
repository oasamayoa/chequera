from django import forms
from .models import Banco, Cuenta, Provedor

class BancoForm(forms.ModelForm):
    class Meta:
        model = Banco
        fields =  ['nombre','estado']
        labels = {'nombre':"Nombre del Banco", 'estado':"Estado"}

        widget={'nombre': forms.TextInput}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class':'form-control'
            })
    def clean(self):
        try:
            sc = Banco.objects.get(
                nombre=self.cleaned_data["nombre"].upper()
            )

            if not self.instance.pk:
                print("Registro ya existe")
                raise forms.ValidationError("Registro Ya Existe")
            elif self.instance.pk!=sc.pk:
                print("Cambio no permitido")
                raise forms.ValidationError("Cambio No Permitido")
        except Banco.DoesNotExist:
            pass
        return self.cleaned_data


class CuentaForm(forms.ModelForm):
    banco = forms.ModelChoiceField(
        queryset=Banco.objects.filter(estado=True)
        .order_by('nombre')
    )
    class Meta:
        model = Cuenta
        fields =  ['banco','nombre','estado']
        labels = {'nombre':"Nombre Cuenta", 'estado':"Estado"}

        widget={'nombre': forms.TextInput}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class':'form-control'
            })

        self.fields['banco'].empty_label = "Selecione el Banco"

class ProveedorForm(forms.ModelForm):
    class Meta:
        model=Provedor
        fields=['nombre', 'estado']
        widget={'nombre': forms.TextInput()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
    def clean(self):
        try:
            sc = Provedor.objects.get(
                nombre=self.cleaned_data["nombre"].upper()
            )

            if not self.instance.pk:
                print("Registro ya existe")
                raise forms.ValidationError("Registro Ya Existe")
            elif self.instance.pk!=sc.pk:
                print("Cambio no permitido")
                raise forms.ValidationError("Cambio No Permitido")
        except Provedor.DoesNotExist:
            pass
        return self.cleaned_data
