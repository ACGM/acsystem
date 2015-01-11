from rest_framework import serializers

from .models import DesembolsoH, DesembolsoD


# Listado de desembolsos
class DesembolsosCajasSerializer(serializers.HyperlinkedModelSerializer):

	class Meta:
		model = DesembolsoH
		fields = ('id', 'beneficiario', 'fecha', 'estatus', 'impreso', 'totalGeneral')
		ordering = ('-id',)