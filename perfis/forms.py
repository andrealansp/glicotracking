from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm

from perfis.models import Perfil, HistoricoPesoImc, HistoricoBioTipo


class RegistroForm(UserCreationForm):

    email = forms.EmailField(label="Email", widget=forms.TextInput, required=True)
    telefone = forms.CharField(label="Telefone", widget=forms.TextInput, required=True)
    first_name = forms.CharField(label="Nome", widget=forms.TextInput, required=True)
    last_name = forms.CharField(label="Sobrenome", widget=forms.TextInput, required=True)
    data_nascimento = forms.DateField(label="Data nascimento",
                                      widget=forms.DateInput(attrs={
                                          'type': 'date',
                                          'class': 'form-control'
                                      }), required=True)
    sexo = forms.ChoiceField(label="Sexo",choices=[('M', 'Masculino'), ('F', 'Femenino')], required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'telefone', 'email', 'sexo', 'data_nascimento', 'password1',
                  'password2')

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")  # Field-specific error
            # Or raise ValidationError("Passwords do not match.") for a non-field error

        return cleaned_data

class PerfilUpdateForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = "__all__"

class HistoricoPesoImcForm(forms.ModelForm):
    class Meta:
        model = HistoricoPesoImc
        fields = ['peso']

class HistoricoBiotipoForm(forms.ModelForm):
    class Meta:
        model = HistoricoBioTipo
        fields = ['cintura','quadril','braco','perna',"abdomen"]