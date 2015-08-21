from django.contrib import admin

from .models import SolicitudPrestamo, SolicitudOrdenDespachoH, SolicitudOrdenDespachoD, DistribucionExcedente, \
					MaestraPrestamo, PrestamoUnificado, PagoCuotasPrestamo, NotaDeCreditoPrestamo, NotaDeCreditoEspecial, \
					NotaDeDebitoPrestamo, InteresPrestamosBaseAhorros


@admin.register(PagoCuotasPrestamo)
class PagoCuotasPrestamoAdmin(admin.ModelAdmin):

	list_display = ['id', 'noPrestamo', 'valorCapital', 'valorInteres', 'fechaPago', 'estatus', 'tipoPago']


@admin.register(NotaDeDebitoPrestamo)
class NotaDeDebitoPrestamoAdmin(admin.ModelAdmin):

	list_display = ['id', 'fecha', 'noPrestamo', 'valorCapital', 'valorInteres', 'concepto', 'estatus', 'posteado', 'fechaPosteo']


@admin.register(NotaDeCreditoPrestamo)
class NotaDeCreditoPrestamoAdmin(admin.ModelAdmin):

	list_display = ['id', 'fecha', 'noPrestamo', 'aplicadoACuota', 'valorCapital', 'valorInteres', 'concepto', 'estatus']


@admin.register(NotaDeCreditoEspecial)
class NotaDeCreditoEspecialAdmin(admin.ModelAdmin):

	list_display = ['id', 'fecha', 'ordenDespacho', 'totalMontoOrden', 'montoConsumido', 'nota', 'estatus', 'posteado', 'fechaPosteo']


@admin.register(SolicitudPrestamo)
class SolicitudPrestamoAdmin(admin.ModelAdmin):

	list_display = ['id', 'noSolicitud', 'fechaSolicitud', 'socio', 'salarioSocio', 'representante', 'cobrador', 'autorizadoPor', \
					'montoSolicitado', 'valorGarantizado', 'netoDesembolsar', 'categoriaPrestamo']


@admin.register(SolicitudOrdenDespachoH)
class SolicitudOrdenDespachoHAdmin(admin.ModelAdmin):

	list_display = ['id', 'noSolicitud', 'fechaSolicitud', 'socio', 'salarioSocio', 'representante', 'cobrador', 'autorizadoPor', \
					'montoSolicitado', 'valorGarantizado', 'netoDesembolsar', 'categoriaPrestamo']


@admin.register(SolicitudOrdenDespachoD)
class SolicitudOrdenDespachoDAdmin(admin.ModelAdmin):

	list_display = ['id', 'ordenDespacho', 'articulo', 'cantidad', 'precio']


@admin.register(MaestraPrestamo)
class MaestraPrestamoAdmin(admin.ModelAdmin):

	list_display = ['noPrestamo', 'fechaDesembolso','noSolicitudPrestamo', 'noSolicitudOD', 'factura', 'categoriaPrestamo', 'socio', 'representante', \
					'oficial', 'localidad', 'montoInicial', 'tasaInteresAnual', 'tasaInteresMensual', 'cantidadCuotas', 'montoCuotaQ1', 'montoCuotaQ2', \
					'usuarioDesembolso', 'valorGarantizado', 'balance', 'quincenas', 'tipoPrestamoNomina', 'archivoBanco', 'estatus', 'valorAhorro']
	search_fields = ('noPrestamo',)


@admin.register(PrestamoUnificado)
class PrestamoUnificadoAdmin(admin.ModelAdmin):

	list_display = ['id', 'solicitudPrestamo', 'prestamoUnificado', 'capitalUnificado', 'estatus']


@admin.register(InteresPrestamosBaseAhorros)
class InteresPrestamosBaseAhorrosAdmin(admin.ModelAdmin):

	list_display = ['id', 'porcentajeAnual', 'estatus']
