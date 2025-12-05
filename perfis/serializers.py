from rest_framework import serializers, generics
from perfis.models import Perfil, HistoricoBioTipo, HistoricoPesoImc

class PerfilSerializer(serializers.ModelSerializer):

    class Meta:
        model = Perfil
        fields = "__all__"

class HistoricoBioTipoSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoricoBioTipo
        fields = "__all__"
