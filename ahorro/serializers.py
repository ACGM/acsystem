from rest_framework import serializers

from .models import MaestraAhorro, AhorroSocio, RetiroAhorro

class maestraAhorroSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model=MaestraAhorro
		many=True
		fields=('fecha','socio','beneficiario','monto','interes','balance','estatus','cuentas')

class AhorroSocioSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model=AhorroSocio
		many=True
		fields=('socio','beneficiario','balance','disponible','cuentas')

class RetiroAhorroSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model=RetiroAhorro
		many=True
		fields=('socio','beneficiario','ahorro','tipoRetiro','monto','cuentas')