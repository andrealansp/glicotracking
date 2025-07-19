from django import forms
from exames.models import Exame

class ExameForm(forms.ModelForm):
    data_exame = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'type': 'date',
                'class': 'form-control'
            }
        ),
        label='Data do Exame'
    )

    class Meta:
        model = Exame
        fields = ["data_exame","medico","especialidade","observacoes","exame_arquivo"]
        widgets = {
            'medico': forms.TextInput(attrs={'class': 'form-control'}),
            'especialidade': forms.TextInput(attrs={'class': 'form-control'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'exame_arquivo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }