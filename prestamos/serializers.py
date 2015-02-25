# SERIALIZERS de PRESTAMOS

from rest_framework import serializers

from administracion.models import Socio, CategoriaPrestamo
from .models import SolicitudPrestamo, SolicitudOrdenDespachoH, SolicitudOrdenDespachoD, DesembolsoElectronico, \
					MaestraPrestamo, PrestamoUnificado, PagoCuotasPrestamo, NotaDeCreditoPrestamo, \
					NotaDeCreditoEspecial, NotaDeDebitoPrestamo, DistribucionExcedente


# Listado de Solicitudes de Prestamos
class SolicitudesPrestamosSerializer(serializers.HyperlinkedModelSerializer):
	socio = serializers.StringRelatedField(read_only=True)
	categoriaPrestamo = serializers.StringRelatedField(read_only=True)

	class Meta:
		model = SolicitudPrestamo
		fields = ('id', 'noSolicitud', 'fechaSolicitud', 'codigoSocio', 'socio', 'montoSolicitado', 'netoDesembolsar', 'categoriaPrestamo', 'estatus')
		ordering = ('-noSolicitud',)


# Listado de Solicitudes de Ordenes de Despacho
class SolicitudesOrdenesDespachoSerializer(serializers.HyperlinkedModelSerializer):
	socio = serializers.StringRelatedField(read_only=True)
	categoriaPrestamo = serializers.StringRelatedField(read_only=True)

	class Meta:
		model = SolicitudOrdenDespachoH
		fields = ('id', 'noSolicitud', 'fechaSolicitud', 'codigoSocio', 'socio', 'montoSolicitado', 'netoDesembolsar', 'categoriaPrestamo', 'estatus')
		ordering = ('-noSolicitud',)


# Listado de Prestamos (Maestra de Prestamos)
class MaestraPrestamosListadoSerializer(serializers.ModelSerializer):
	factura = serializers.StringRelatedField(read_only=True)
	socio = serializers.StringRelatedField(read_only=True)
	categoriaPrestamo = serializers.StringRelatedField(read_only=True)

	class Meta:
		model = MaestraPrestamo
		fields = ('noPrestamo', 'estatus', 'factura', 'codigoSocio', 'socio', 'montoInicial', 'categoriaPrestamo')
		ordering = ('-noPrestamo',)


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