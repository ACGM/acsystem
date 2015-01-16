from rest_framework import serializers

from .models import NominaCoopH, NominaCoopD


# Listado de Nominas Generadas
class NominasGeneradasSerializer(serializers.HyperlinkedModelSerializer):
	tipoNomina = serializers.StringRelatedField(read_only=True)

	class Meta:
		model = NominaCoopH
		fields = ('id', 'fechaNomina', 'fechaPago', 'valorNomina', 'tipoNomina', 'tipoPago', 'estatus', 'quincena', 'cntEmpleados')
		ordering = ('-fechaNomina',)