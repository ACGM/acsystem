from rest_framework import serializers

from .models import DesembolsoH, DesembolsoD
from administracion.models import Localidad


# Listado de desembolsos
class DesembolsosCajasSerializer(serializers.HyperlinkedModelSerializer):
	localidad = serializers.StringRelatedField(read_only=True)

	class Meta:
		model = DesembolsoH
		fields = ('id', 'beneficiario', 'localidad', 'fecha', 'cheque', 'estatus', 'impreso', 'totalGeneral')
		ordering = ('-id',)