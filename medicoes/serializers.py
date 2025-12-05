from medicoes.models import Medicao
from rest_framework import serializers

class MedicaoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Medicao
        fields = '__all__'
