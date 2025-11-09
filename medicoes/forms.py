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
                  'exame']
        widgets = {
            'data_medicao': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class MedicaoFilterForm(forms.Form):

    MESES = [("","Todos os Meses"),("01","janeiro"),("02","fevereiro"),("03","março"),("04","abril"),
             ("05","maio"),("06","junho"),("07","julho"),("08","agosto"),
             ("09","setembro"),("10","outubro"),("11","Novembro"),("12","dezembro")]

    tipo_medicao = forms.ChoiceField(label="Tipo de Medição", choices=Medicao.TIPO_MEDICAO_CHOICES, required=False)
    mes = forms.ChoiceField(required=False, choices=MESES)

    class Meta:
        fields = ['tipo_medicao',"data_medicao"]

        widgets = {
            'data_medicao': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }