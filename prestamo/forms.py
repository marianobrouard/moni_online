from django import forms
from .models import Prestamo

class NuevoPrestamoForm(forms.ModelForm):

    class Meta:
        model = Prestamo
        fields = ['dni','nombre','apellido','genero','email','monto_solicitado']
        genero_choice = (
            ('0', 'MASCULINO'),
            ('1', 'FEMENINO'),
        )
        widgets = {
            'dni':forms.TextInput(attrs={'class':'form-control','type':'number'}),
            'nombre':forms.TextInput(attrs={'class':'form-control','pattern':'[A-Za-z ]+'}),
            'apellido':forms.TextInput(attrs={'class':'form-control','pattern':'[A-Za-z ]+'}),
            'genero':forms.Select(attrs={"name": "select_0","class": "form-control"}),
            'email':forms.TextInput(attrs={'class':'form-control'}),
            'monto_solicitado':forms.TextInput(attrs={'class':'form-control'}),
        }


    def clean_monto_solicitado(self):
        monto_solicitado = self.cleaned_data['monto_solicitado']
        if monto_solicitado < 1000.00:
            raise forms.ValidationError('EL monto solicitado no puede ser menor a 1.000 pesos')
        if monto_solicitado > 65000.00:
            raise forms.ValidationError('EL monto solicitado no puede ser mayor a 65.000 pesos')
        if type(monto_solicitado) is float:
            raise forms.ValidationError('EL monto solicitado debe ser un número')
        return monto_solicitado
    

    def clean_dni(self):
        dni = self.cleaned_data['dni']
        if len(str(dni)) < 8:
            raise forms.ValidationError('EL DNI debe contener más de 8 caratacteres')
        if len(str(dni)) > 9:
            raise forms.ValidationError('EL DNI no debe contener más de 8 caratacteres')
        return dni  
    



