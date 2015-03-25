from rest_framework import serializers

from .models import DesembolsoH, DesembolsoD
from administracion.models import Localidad


# Listado de desembolsos
class DesembolsosCajasSerializer(serializers.HyperlinkedModelSerializer):
	localidad = serializers.StringRelatedField(read_only=True)
	fondo = serializers.StringRelatedField(read_only=True)

	class Meta:
		model = DesembolsoH
		fields = ('id', 'fecha', 'fondo', 'localidad', 'detalle', 'concepto', 'estatus', 'impreso', 'cheque', 'totalGeneral')
		ordering = ('-id',)