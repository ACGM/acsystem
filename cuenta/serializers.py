from rest_framework import serializers

from .models import Cuentas, DiarioGeneral, CuentasControl, BalanceCuenta
from administracion.models import TipoDocumento


class CuentasControlSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CuentasControl
        fields = ('codigoControl', 'descripcion')


class CuentasSerializer(serializers.HyperlinkedModelSerializer):
    cuentaControl = serializers.StringRelatedField()

    class Meta:
        model = Cuentas
        fields = ('codigo', 'descripcion', 'origen', 'control', 'tipo' ,'cuentaControl', 'tipoSocio')
        ordering = ('origen')


class DiarioSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DiarioGeneral
        many = True
        fields = ('id', 'fecha', 'cuenta', 'referencia', 'tipoDoc', 'debito', 'credito', 'estatus')

class BalanceSerializar(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = BalanceCuenta
        many = True
        fields = ('id', 'agno', 'mes', 'cuenta', 'balance')

