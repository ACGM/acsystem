from rest_framework import serializers

from .models import SolicitudPrestamo, SolicitudOrdenDespachoH, SolicitudOrdenDespachoD, DesembolsoElectronico, \
					MaestraPrestamo, PrestamoUnificado, CuotasPrestamo, NotaDeCreditoPrestamo, NotaDeCreditoEspecial, \
					NotaDeDebitoPrestamo, DistribucionExcedente


# Listado de Solicitudes de Prestamos
class SolicitudesPrestamosSerializer(serializers.HyperlinkedModelSerializer):
	socio = serializers.StringRelatedField(read_only=True)
	categoriaPrestamo = serializers.StringRelatedField(read_only=True)

	class Meta:
		model = SolicitudPrestamo
		fields = ('id', 'noSolicitud', 'fechaSolicitud', 'codigoSocio', 'socio', 'montoSolicitado', 'netoDesembolsar', 'categoriaPrestamo', 'estatus')
		ordering = ('-fechaSolicitud', '-noSolicitud')


# Listado de Solicitudes de Ordenes de Despacho
class SolicitudesOrdenesDespachoSerializer(serializers.HyperlinkedModelSerializer):

	pass


# Listado de Prestamos (Maestra de Prestamos)
class MaestraPrestamosListado(serializers.HyperlinkedModelSerializer):

	pass


# Prestamos Unificados
class PrestamosUnificados(serializers.HyperlinkedModelSerializer):

	pass


# Cuotas de Prestamos
class CuotasPrestamos(serializers.HyperlinkedModelSerializer):

	pass


# Notas de Credito a Prestamos
class NotasCreditoListado(serializers.HyperlinkedModelSerializer):

	pass


# Notas de Credito Especiales a Prestamos
class NotasCreditoEspecialesListado(serializers.HyperlinkedModelSerializer):

	pass


# Notas de Debito a Prestamos
class NotasDebitoListado(serializers.HyperlinkedModelSerializer):

	pass


# Listado de Desembolsos Electronicos
class DesembolsosElectronicos(serializers.HyperlinkedModelSerializer):

	class Meta:
		model = DesembolsoElectronico


# Distribucion de Excedentes (proceso de calculos de interes - Anual)
class DistribucionExcedenteListado(serializers.HyperlinkedModelSerializer):

	pass