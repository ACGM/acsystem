from django.contrib import admin

from .models import SolicitudPrestamo, SolicitudOrdenDespachoH, SolicitudOrdenDespachoD, DistribucionExcedente, \
					MaestraPrestamo, PrestamoUnificado, PagoCuotasPrestamo, NotaDeCreditoPrestamo, NotaDeCreditoEspecial, \
					NotaDeDebitoPrestamo

@admin.register(NotaDeDebitoPrestamo)
class NotaDeDebitoPrestamoAdmin(admin.ModelAdmin):

	list_display = ['id', 'fecha', 'noPrestamo', 'valorCapital', 'valorInteres', 'concepto', 'estatus']


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

	list_display = ['noPrestamo', 'fechaDesembolso','noSolicitudPrestamo', 'noSolicitudOD', 'factura', 'categoriaPrestamo', 'socio']
	search_fields = ('noPrestamo',)
