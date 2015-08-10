from rest_framework import serializers

from .models import InteresesAhorro, MaestraAhorro, AhorroSocio


class interesAhorroSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = InteresesAhorro
        many = False
        fields = ('id', 'descripcion', 'porcentaje')


class maestraAhorroSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MaestraAhorro
        many = True
        fields = ('id', 'fecha', 'ahorro',  'monto',  'estatus', 'cuentas')


class AhorroSocioSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = AhorroSocio
        many = True
        fields = ('id', 'socio', 'balance', 'disponible')
