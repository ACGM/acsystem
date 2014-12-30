from rest_framework import serializers

from .models import SolicitudCheque, ConcCheques, NotaDCConciliacion

class solicitudSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model=SolicitudCheque
		many=True
		fields=('id','fecha','socio','beneficiario','concepto','monto','cuentas')

class chequesSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model=ConcCheques
		many=True
		fields=('id','solicitud','chequeNo','fecha','estatus')

class NotasSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model=NotaDCConciliacion
		many=True
		fields=('id','concepto', 'fecha', 'tipo', 'monto', 'estatus', 'cuentas')
