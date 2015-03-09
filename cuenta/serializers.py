from rest_framework import serializers

from .models import Cuentas, Auxiliares, DiarioGeneral, TipoDocumento, CuentasControl


class CuentasControlSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CuentasControl
        fields = ('codigoControl', 'descripcion')


class CuentasSerializer(serializers.HyperlinkedModelSerializer):
    cuentaControl = serializers.StringRelatedField()

    class Meta:
        model = Cuentas
        fields = ('codigo', 'descripcion', 'origen', 'control', 'cuentaControl')


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


class TipoDocSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TipoDocumento
        many = False
        field = ("tipoDoc", "descripcion")