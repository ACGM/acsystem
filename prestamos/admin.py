from django.contrib import admin

from .models import SolicitudPrestamo, SolicitudOrdenDespachoH, SolicitudOrdenDespachoD, DesembolsoElectronico, \
					MaestraPrestamo, PrestamoUnificado, PagoCuotasPrestamo, NotaDeCreditoPrestamo, NotaDeCreditoEspecial, \
					NotaDeDebitoPrestamo, DistribucionExcedente

@admin.register(SolicitudPrestamo)
class SolicitudPrestamoAdmin(admin.ModelAdmin):

	list_display = ['id', 'noSolicitud', 'fechaSolicitud', 'socio', 'salarioSocio', 'representante', 'cobrador', 'autorizadoPor', \
					'montoSolicitado', 'valorGarantizado', 'netoDesembolsar', 'categoriaPrestamo']


@admin.register(SolicitudOrdenDespachoH)
class SolicitudOrdenDespachoHAdmin(admin.ModelAdmin):

	list_display = ['id', 'noSolicitud', 'fechaSolicitud', 'socio', 'salarioSocio', 'representante', 'cobrador', 'autorizadoPor', \
					'montoSolicitado', 'valorGarantizado', 'netoDesembolsar', 'categoriaPrestamo']


@admin.register(MaestraPrestamo)
class MaestraPrestamoAdmin(admin.ModelAdmin):

	list_display = ['id','noPrestamo','noSolicitudPrestamo', 'noSolicitudOD', 'factura', 'categoriaPrestamo', 'socio']
