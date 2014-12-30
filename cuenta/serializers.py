from rest_framework import serializers

from .models import Cuentas, Auxiliares, DiarioGeneral


class CuentasSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model=Cuentas
		fields=('codigo','descripcion','origen')


class AuxiliarSerualizer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model=Auxiliares
		fields=('codigo','descripcion','cuenta')

class DiarioSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model=DiarioGeneral
		many=True
		fields=('fecha', 'cuenta','auxiliar', 'referencia', 'tipoDoc', 'estatus','debito', 'credito')