from rest_framework import serializers

from .models import Cuentas, Auxiliares, DiarioGeneral, CuentasControl
from administracion.models import TipoDocumento


class CuentasControlSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CuentasControl
        fields = ('codigoControl', 'descripcion')


class CuentasSerializer(serializers.HyperlinkedModelSerializer):
    cuentaControl = serializers.StringRelatedField()

    class Meta:
        model = Cuentas
        fields = ('codigo', 'descripcion', 'origen', 'control', 'tipo' ,'cuentaControl')


class AuxiliarSerializer(serializers.HyperlinkedModelSerializer):
    cuenta = serializers.StringRelatedField()

    class Meta:
        model = Auxiliares
        fields = ('codigo', 'descripcion', 'cuenta')


class DiarioSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DiarioGeneral
        many = True
        fields = ('id', 'fecha', 'cuenta', 'auxiliar', 'referencia', 'tipoDoc', 'debito', 'credito', 'estatus')

