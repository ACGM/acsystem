from rest_framework import serializers

from .models import InteresesAhorro, MaestraAhorro, AhorroSocio


class interesAhorroSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = InteresesAhorro
        many = False
        fields = ('id', 'descripcion', 'porcentaje')


class maestraAhorroSerializer(serializers.HyperlinkedModelSerializer):
    cuenta = serializers.StringRelatedField(read_only = True)
    class Meta:
        model = MaestraAhorro
        many = True
        fields = ('id', 'fecha', 'ahorro',  'monto',  'estatus', 'cuenta')


class AhorroSocioSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = AhorroSocio
        many = True
        fields = ('id', 'socio', 'balance', 'disponible')
