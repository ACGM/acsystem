from rest_framework import serializers

from .models import InteresesAhorro , MaestraAhorro, AhorroSocio, RetiroAhorro

class interesAhorroSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model=InteresesAhorro
		many=False
		fields=('descripcion','porcentaje')
		
class maestraAhorroSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model=MaestraAhorro
		many=True
		fields=('id','fecha','ahorro','retiro','monto','interes','balance','estatus','cuentas')

class AhorroSocioSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model=AhorroSocio
		many=True
		fields=('id','socio','balance','disponible')

class RetiroAhorroSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model=RetiroAhorro
		many=True
		fields=('id','socio','ahorro','tipoRetiro','monto')