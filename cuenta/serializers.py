from rest_framework import serializers

from .models import Cuentas, Auxiliares, DiarioGeneral, TipoDocumento, CuentasControl


class CuentasControlSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model=CuentasControl
		fields=('codigoControl','descripcion')

class CuentasSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model=Cuentas
		fields=('codigo','descripcion','origen','control','cuentaControl')


class AuxiliarSerualizer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model=Auxiliares
		fields=('codigo','descripcion','cuenta')

class DiarioSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model=DiarioGeneral
		many=True
		fields=('fecha', 'cuenta','auxiliar', 'referencia', 'tipoDoc', 'estatus','debito', 'credito')

class TipoDocSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model=TipoDocumento
		many=False
		field=("tipoDoc","descripcion")