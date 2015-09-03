# SERIALIZERS de PRESTAMOS

from rest_framework import serializers

from administracion.models import Socio, CategoriaPrestamo
from .models import SolicitudPrestamo, SolicitudOrdenDespachoH, SolicitudOrdenDespachoD, DistribucionExcedente, \
					MaestraPrestamo, PrestamoUnificado, PagoCuotasPrestamo, NotaDeCreditoPrestamo, \
					NotaDeCreditoEspecial, NotaDeDebitoPrestamo, InteresPrestamosBaseAhorros


# Listado de Solicitudes de Prestamos
class SolicitudesPrestamosSerializer(serializers.HyperlinkedModelSerializer):
	socio = serializers.StringRelatedField(read_only=True)
	categoriaPrestamo = serializers.StringRelatedField(read_only=True)
	representante = serializers.StringRelatedField(read_only=True)

	class Meta:
		model = SolicitudPrestamo
		fields = ('id', 'noSolicitud', 'fechaSolicitud', 'codigoSocio', 'socio', 'montoSolicitado', 'netoDesembolsar',  \
					'categoriaPrestamo', 'estatus', 'representante', 'tasaInteresMensual', 'cantidadCuotas', 'valorCuotasCapital', \
					'ahorrosCapitalizados', 'prestacionesLaborales', 'valorGarantizado', 'deudasPrestamos', 'codigoRepresentante', \
					'codigoCategoria', 'interesBaseAhorroMensual')
		ordering = ('-noSolicitud',)


# Listado de Solicitudes de Ordenes de Despacho
class SolicitudesOrdenesDespachoSerializer(serializers.HyperlinkedModelSerializer):
	socio = serializers.StringRelatedField(read_only=True)
	categoriaPrestamo = serializers.StringRelatedField(read_only=True)
	suplidor = serializers.StringRelatedField(read_only=True)

	class Meta:
		model = SolicitudOrdenDespachoH
		fields = ('id', 'noSolicitud', 'fechaSolicitud', 'codigoSocio', 'socio', 'montoSolicitado', 'netoDesembolsar', 'categoriaPrestamo', 'estatus', 'suplidor')
		ordering = ('-noSolicitud',)


# Listado de Prestamos (Maestra de Prestamos)
class MaestraPrestamosListadoSerializer(serializers.ModelSerializer):
	factura = serializers.StringRelatedField(read_only=True)
	socio = serializers.StringRelatedField(read_only=True)
	categoriaPrestamo = serializers.StringRelatedField(read_only=True)

	class Meta:
		model = MaestraPrestamo
		fields = ('noPrestamo', 'estatus', 'factura', 'codigoSocio', 'socio', 'montoInicial', 'categoriaPrestamo', 'balance', 'noSolicitudPrestamo', \
					'noSolicitudOD', 'montoCuotaQ1', 'montoCuotaQ2', 'tasaInteresMensual', 'cuotaInteresQ1', 'cuotaInteresQ2', 'cuotaMasInteresQ1', \
					'cuotaMasInteresQ2', 'tipoPrestamoNomina', 'cuotaInteresAhQ1', 'cuotaInteresAhQ2', 'documentoDescrp')
		ordering = ('-noPrestamo',)


# Listado de Prestamos (Balance Socio)
class BalancePrestamosSocioSerializer(serializers.ModelSerializer):
	socio = serializers.StringRelatedField(read_only=True)

	class Meta:
		model = MaestraPrestamo
		fields = ('codigoSocio', 'socio', 'balance')
		ordering = ('-codigoSocio',)


# Listado de Pagos de Cuotas Prestamos 
class PagoCuotasPrestamoSerializer(serializers.ModelSerializer):
	noPrestamo = serializers.StringRelatedField(read_only=True)

	class Meta:
		model = PagoCuotasPrestamo
		fields = ('id', 'noPrestamo', 'valorCapital', 'valorInteres', 'fechaPago', 'tipoPago')
		ordering = ('-id',)


# Prestamos Unificados
class PrestamosUnificados(serializers.HyperlinkedModelSerializer):

	pass


# Cuotas de Prestamos
class CuotasPrestamos(serializers.HyperlinkedModelSerializer):

	pass


# Notas de Credito a Prestamos
class NotasCreditoListado(serializers.HyperlinkedModelSerializer):
	noPrestamo = serializers.StringRelatedField(read_only=True)
	aplicadoACuota = serializers.StringRelatedField(read_only=True)

	class Meta:
		model = NotaDeCreditoPrestamo
		fields = ('id', 'fecha', 'noPrestamo', 'aplicadoACuota', 'valorCapital', 'valorInteres', 'concepto', 'posteado', 'getSocio')
		ordering = ('-fecha',)


# Notas de Credito Especiales a Prestamos
class NotasCreditoEspecialesListado(serializers.HyperlinkedModelSerializer):
	ordenDespacho = serializers.StringRelatedField(read_only=True)

	class Meta:
		model = NotaDeCreditoEspecial
		fields = ('id', 'fecha', 'ordenDespacho', 'totalMontoOrden', 'montoConsumido', 'nota', 'estatus', 'posteado', \
					'fechaPosteo', 'getSocio', 'getMontoAhorro')
		ordering = ('-fecha')


# Notas de Debito a Prestamos
class NotasDebitoListado(serializers.HyperlinkedModelSerializer):
	noPrestamo = serializers.StringRelatedField(read_only=True)

	class Meta:
		model = NotaDeDebitoPrestamo
		fields = ('id', 'fecha', 'noPrestamo', 'valorCapital', 'valorInteres', 'concepto', 'estatus', 'posteado')
		ordering = ('-fecha',)


# Interes de Prestamo en Base Ahorros
class InteresPrestamoBaseAhorroSerializer(serializers.ModelSerializer):

	class Meta:
		model = InteresPrestamosBaseAhorros
		fields = ('id', 'porcentajeAnual', 'estatus')


# Distribucion de Excedentes (proceso de calculos de interes - Anual)
class DistribucionExcedenteListado(serializers.HyperlinkedModelSerializer):

	pass