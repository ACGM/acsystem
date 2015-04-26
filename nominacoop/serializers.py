from rest_framework import serializers

from .models import NominaCoopH, NominaCoopD, TipoNomina


# Listado de Nominas Generadas
class NominasGeneradasSerializer(serializers.HyperlinkedModelSerializer):
	tipoNomina = serializers.StringRelatedField(read_only=True)

	class Meta:
		model = NominaCoopH
		fields = ('id', 'fechaNomina', 'fechaPago', 'tipoNomina', 'tipoPago', 'estatus', 'quincena', 'nota', \
		 'cntEmpleados', 'valorNomina', 'sueldoMensual', 'ISR', 'AFP', 'ARS', 'CAFETERIA', 'VACACIONES', \
		 'OTROSINGRESOS', 'DESCAHORROS', 'DESCPRESTAMOS', 'posteada')
		ordering = ('-id',)


# Detalle de Nomina
class NominaGeneradaDetalleSerializer(serializers.HyperlinkedModelSerializer):
	empleado = serializers.StringRelatedField(read_only=True)
	nomina = serializers.StringRelatedField(read_only=True)

	class Meta:
		model = NominaCoopD
		fields = ('id', 'nomina', 'getcodigo', 'empleado', 'salario', 'isr', 'afp', 'ars', 'cafeteria', 'horasExtras', \
					'vacaciones', 'otrosIngresos', 'descAhorros', 'descPrestamos', 'pago','tipoPago', 'estatus', 'getCuentaBanco')
		ordering = ('empleado',)


# Tipos de Nominas
class TiposNominasSerializer(serializers.HyperlinkedModelSerializer):

	class Meta:
		model = TipoNomina
		fields = ('id','descripcion',)