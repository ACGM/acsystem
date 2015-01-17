from rest_framework import serializers

from .models import NominaCoopH, NominaCoopD, TipoNomina


# Listado de Nominas Generadas
class NominasGeneradasSerializer(serializers.HyperlinkedModelSerializer):
	tipoNomina = serializers.StringRelatedField(read_only=True)

	class Meta:
		model = NominaCoopH
		fields = ('id', 'fechaNomina', 'fechaPago', 'tipoNomina', 'tipoPago', 'estatus', 'quincena', 'cntEmpleados', 'valorNomina')
		ordering = ('-id',)


# Detalle de Nomina
class NominaGeneradaDetalleSerializer(serializers.HyperlinkedModelSerializer):
	empleado = serializers.StringRelatedField(read_only=True)
	nomina = serializers.StringRelatedField(read_only=True)

	class Meta:
		model = NominaCoopD
		fields = ('id', 'nomina', 'empleado', 'salario', 'isr', 'afp', 'ars', 'cafeteria', \
					'vacaciones', 'otrosIngresos', 'descAhorros', 'descPrestamos', 'tipoPago', 'estatus')
		ordering = ('empleado',)


# Tipos de Nominas
class TiposNominasSerializer(serializers.HyperlinkedModelSerializer):

	class Meta:
		model = TipoNomina
		fields = ('id','descripcion',)