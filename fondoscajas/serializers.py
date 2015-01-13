from rest_framework import serializers

from .models import DesembolsoH, DesembolsoD
from administracion.models import Distrito


# Listado de desembolsos
class DesembolsosCajasSerializer(serializers.HyperlinkedModelSerializer):
	distrito = serializers.StringRelatedField(read_only=True)

	class Meta:
		model = DesembolsoH
		fields = ('id', 'beneficiario', 'distrito', 'fecha', 'cheque', 'estatus', 'impreso', 'totalGeneral')
		ordering = ('-id',)