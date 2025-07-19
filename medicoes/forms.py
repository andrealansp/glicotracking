from tabnanny import verbose

from django import forms

from .models import Medicao


class MedicaoForm(forms.ModelForm):
    class Meta:
        model = Medicao
        fields = ['valor_glicose',
                  'tipo_medicao',
                  'data_medicao',
                  'observacoes',
                  'alimento',
                  'tipo_refeicao',
                  'tamanho',
                  'exame']
        widgets = {
            'data_medicao': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class MedicaoFilterForm(forms.Form):

    tipo_medicao = forms.ChoiceField(label="Tipo de Medição", choices=Medicao.TIPO_MEDICAO_CHOICES, required=False)
    data_medicao = forms.DateTimeField(required=False)

    class Meta:
        fields = ['tipo_medicao',"data_medicao"]

        widgets = {
            'data_medicao': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }